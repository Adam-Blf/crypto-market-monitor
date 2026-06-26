import { useState, useEffect, useRef, useCallback, useMemo } from 'react';
import type { AlertConfig, Metrics, CryptoSymbol } from '../types';
import { SYMBOLS } from '../types';

const STORAGE_KEY = 'cmm-alerts';

function loadAlerts(): AlertConfig[] {
  const defaults = SYMBOLS.map(sym => ({ symbol: sym, enabled: false }));
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return defaults;
    const parsed: AlertConfig[] = JSON.parse(raw);
    // Merge: backfill any new symbols added after a previous save
    const bySymbol = new Map(parsed.map(a => [a.symbol, a]));
    return SYMBOLS.map(sym => bySymbol.get(sym) ?? { symbol: sym, enabled: false });
  } catch (_) { /* localStorage indisponible en mode prive? */ }
  return defaults;
}

function saveAlerts(alerts: AlertConfig[]) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(alerts));
}

export function useAlerts(metrics: Record<string, Metrics>) {
  const [alerts, setAlerts] = useState<AlertConfig[]>(loadAlerts);
  const [triggered, setTriggered] = useState<string[]>([]);

  // Cooldown par symbole: evite le spam de notifications si le prix reste hors seuil
  const cooldownRef = useRef<Record<string, number>>({});

  const updateAlert = useCallback((symbol: CryptoSymbol, patch: Partial<AlertConfig>) => {
    setAlerts(prev => {
      const next = prev.map(a => a.symbol === symbol ? { ...a, ...patch } : a);
      saveAlerts(next);
      return next;
    });
  }, []);

  useEffect(() => {
    const now = Date.now();
    const newTriggered: string[] = [];

    for (const alert of alerts) {
      if (!alert.enabled) continue;
      const m = metrics[alert.symbol];
      if (!m) continue;

      // 30 secondes de silence apres une alerte pour le meme symbole
      const cooldown = cooldownRef.current[alert.symbol] ?? 0;
      if (now - cooldown < 30_000) continue;

      let fired = false;
      let message = '';

      if (alert.priceAbove != null && m.currentPrice > alert.priceAbove) {
        fired = true;
        message = `${alert.symbol} > ${alert.priceAbove.toLocaleString()} $ (${m.currentPrice.toFixed(2)} $)`;
      } else if (alert.priceBelow != null && m.currentPrice < alert.priceBelow) {
        fired = true;
        message = `${alert.symbol} < ${alert.priceBelow.toLocaleString()} $ (${m.currentPrice.toFixed(2)} $)`;
      } else if (alert.zscoreAbove != null && (m.anomalyScore ?? 0) > alert.zscoreAbove) {
        fired = true;
        message = `Anomalie ${alert.symbol} z=${(m.anomalyScore ?? 0).toFixed(2)} > ${alert.zscoreAbove}`;
      }

      if (fired) {
        cooldownRef.current[alert.symbol] = now;
        newTriggered.push(message);
        // Notification navigateur si l'utilisateur a donne la permission
        if ('Notification' in window && Notification.permission === 'granted') {
          new Notification('Crypto Monitor - Alerte', { body: message, icon: '/icons/bitcoin.svg' });
        }
      }
    }

    if (newTriggered.length > 0) {
      setTriggered(prev => [...newTriggered, ...prev].slice(0, 20));
    }
  }, [metrics, alerts]);

  const requestPermission = useCallback(() => {
    if ('Notification' in window && Notification.permission === 'default') {
      Notification.requestPermission();
    }
  }, []);

  const activeCount = useMemo(() => alerts.filter(a => a.enabled).length, [alerts]);

  return { alerts, updateAlert, triggered, activeCount, requestPermission };
}
