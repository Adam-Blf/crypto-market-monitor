import { Trade } from './types';

// Buffer circulaire en memoire par symbole - pas de persistence intentionnelle
// On garde 10 minutes de trades max, suffisant pour VWAP 1min et variation 5min
const MAX_TRADES_PER_SYMBOL = 1000;
const EVICTION_WINDOW_MS = 10 * 60 * 1000;

const store = new Map<string, Trade[]>();

export function addTrade(trade: Trade): void {
  const symbol = trade.symbol;
  if (!store.has(symbol)) {
    store.set(symbol, []);
  }

  const trades = store.get(symbol)!;
  trades.push(trade);

  // Hard cap: eviction par shift() = O(n) mais acceptable pour 1000 elements
  if (trades.length > MAX_TRADES_PER_SYMBOL) {
    trades.shift();
  }

  // Eviction temporelle: on nettoie les trades trop vieux a chaque insertion
  // Ca evite de garder des trades d'une session precedente si le process redémarre
  const cutoff = Date.now() - EVICTION_WINDOW_MS;
  while (trades.length > 0 && trades[0].timestamp < cutoff) {
    trades.shift();
  }
}

export function getTradesInWindow(symbol: string, windowMs: number): Trade[] {
  const trades = store.get(symbol);
  if (!trades || trades.length === 0) return [];

  const cutoff = Date.now() - windowMs;
  return trades.filter((t) => t.timestamp >= cutoff);
}

// getLastN sert pour le SMA-20: on veut les 20 derniers trades, pas une fenetre temporelle
export function getLastN(symbol: string, n: number): Trade[] {
  const trades = store.get(symbol);
  if (!trades || trades.length === 0) return [];
  return trades.slice(-n);
}

export function getSymbols(): string[] {
  return Array.from(store.keys());
}
