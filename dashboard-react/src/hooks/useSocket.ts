import { useState, useEffect, useRef, useCallback } from 'react';
import { io, Socket } from 'socket.io-client';
import type { Metrics, AnomalyEvent, CryptoSymbol } from '../types';
import { API_URL, SYMBOLS, MAX_CHART_POINTS, MAX_ANOMALIES } from '../types';
import { playAnomalyBeep } from '../utils';

// Prix de base pour le mode demo (approximations des cours recents)
const DEMO_BASE: Record<string, number> = {
  'BTC-USDT': 67432.18,
  'ETH-USDT': 3521.44,
  'BTC-USD': 67389.92,
  'SOL-USDT': 178.54,
  'BNB-USDT': 612.30,
  'XRP-USDT': 0.5823,
};

// Genere des metriques realistes pour la demo sans backend
function buildMockMetrics(symbol: string, prevPrice?: number): Metrics {
  const base = DEMO_BASE[symbol] || 50000;
  // Variation aleatoire faible pour simuler un marche liquide
  const price = (prevPrice || base) + (Math.random() - 0.5) * 30;
  return {
    symbol,
    timestamp: Date.now(),
    currentPrice: price,
    vwap: base * (1 + (Math.random() - 0.5) * 0.001),
    sma20: base * (1 + (Math.random() - 0.5) * 0.002),
    priceChange1m: (Math.random() - 0.48) * 0.8,
    priceChange5m: (Math.random() - 0.45) * 1.5,
    volumeTotal1m: Math.floor(Math.random() * 5_000_000 + 1_000_000),
    tradeCount1m: Math.floor(Math.random() * 400 + 100),
    highPrice1m: base * 1.003,
    lowPrice1m: base * 0.997,
    anomaly: false,
    anomalyScore: 0.5,
  };
}

export interface SocketState {
  connected: boolean;
  demoMode: boolean;
  metrics: Record<string, Metrics>;
  history: Record<string, Metrics[]>;
  anomalies: AnomalyEvent[];
  serverStats: string;
  msgCount: number;
}

export function useSocket(currentSymbol: CryptoSymbol) {
  const [state, setState] = useState<SocketState>({
    connected: false,
    demoMode: false,
    metrics: {},
    history: {},
    anomalies: [],
    serverStats: '0 msg/s',
    msgCount: 0,
  });

  const socketRef = useRef<Socket | null>(null);
  const demoIntervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const pushHistory = useCallback((sym: string, m: Metrics, prev: Record<string, Metrics[]>) => {
    const arr = [...(prev[sym] || []), m];
    return { ...prev, [sym]: arr.length > MAX_CHART_POINTS ? arr.slice(-MAX_CHART_POINTS) : arr };
  }, []);

  const startDemo = useCallback(() => {
    // Seed 60 points d'historique pour que le graphe ne soit pas vide au demarrage
    setState(s => {
      let metrics = { ...s.metrics };
      let history = { ...s.history };
      SYMBOLS.forEach(sym => {
        for (let i = 0; i < 60; i++) {
          const m = buildMockMetrics(sym, metrics[sym]?.currentPrice);
          history = { ...history, [sym]: [...(history[sym] || []), m].slice(-MAX_CHART_POINTS) };
          metrics = { ...metrics, [sym]: m };
        }
      });
      return { ...s, demoMode: true, metrics, history };
    });

    // Premiere anomalie seeder apres 800ms pour demo le flux d'alertes
    setTimeout(() => {
      setState(s => ({
        ...s,
        anomalies: [{
          symbol: 'BTC-USDT',
          timestamp: Date.now() - 12000,
          currentPrice: 68105.77,
          anomalyScore: 3.12,
        }, ...s.anomalies].slice(0, MAX_ANOMALIES),
      }));
      playAnomalyBeep();
    }, 800);

    demoIntervalRef.current = setInterval(() => {
      setState(s => {
        const sym = SYMBOLS[Math.floor(Math.random() * SYMBOLS.length)];
        const m = buildMockMetrics(sym, s.metrics[sym]?.currentPrice);
        const history = pushHistory(sym, m, s.history);
        return {
          ...s,
          metrics: { ...s.metrics, [sym]: m },
          history,
          msgCount: s.msgCount + 1,
        };
      });
    }, 800);
  }, [pushHistory]);

  const fetchHistory = useCallback(async (sym: string) => {
    try {
      const res = await fetch(`${API_URL}/api/history/${sym}?limit=${MAX_CHART_POINTS}`);
      if (!res.ok) return;
      const data: Metrics[] = await res.json();
      if (Array.isArray(data)) {
        setState(s => ({ ...s, history: { ...s.history, [sym]: data } }));
      }
    } catch (_) { /* serveur pas encore pret, mode demo prendra le relai */ }
  }, []);

  useEffect(() => {
    const socket = io(API_URL, {
      reconnectionDelay: 1000,
      reconnectionDelayMax: 5000,
      transports: ['websocket', 'polling'],
      timeout: 3000,
    });
    socketRef.current = socket;

    // Si pas connecte apres 3s, on bascule en mode demo automatiquement
    const demoTimer = setTimeout(() => {
      if (!socket.connected) startDemo();
    }, 3000);

    socket.on('connect', () => {
      clearTimeout(demoTimer);
      if (demoIntervalRef.current) { clearInterval(demoIntervalRef.current); demoIntervalRef.current = null; }
      setState(s => ({ ...s, connected: true, demoMode: false }));
      socket.emit('subscribe:symbol', currentSymbol);
      fetchHistory(currentSymbol);
    });

    socket.on('disconnect', () => setState(s => ({ ...s, connected: false })));
    socket.on('connect_error', () => setState(s => ({ ...s, connected: false })));

    socket.on('metrics:update', (m: Metrics) => {
      setState(s => {
        const history = pushHistory(m.symbol, m, s.history);
        return {
          ...s,
          metrics: { ...s.metrics, [m.symbol]: m },
          history,
          msgCount: s.msgCount + 1,
        };
      });
    });

    socket.on('anomaly:detected', (m: AnomalyEvent) => {
      setState(s => ({
        ...s,
        anomalies: [m, ...s.anomalies].slice(0, MAX_ANOMALIES),
      }));
      playAnomalyBeep();
    });

    socket.on('server:stats', (stats: { connections?: number; msgsPerSec?: number }) => {
      setState(s => ({
        ...s,
        serverStats: `${stats.connections ?? '-'} clients - ${stats.msgsPerSec ?? '-'} msg/s`,
      }));
    });

    return () => {
      clearTimeout(demoTimer);
      if (demoIntervalRef.current) clearInterval(demoIntervalRef.current);
      socket.disconnect();
    };
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  // Ré-abonnement quand l'utilisateur change de symbole dans les tabs
  useEffect(() => {
    if (socketRef.current?.connected) {
      socketRef.current.emit('subscribe:symbol', currentSymbol);
      fetchHistory(currentSymbol);
    }
  }, [currentSymbol, fetchHistory]);

  return state;
}
