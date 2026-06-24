import { Trade } from './types';

const MAX_TRADES_PER_SYMBOL = 1000;
const EVICTION_WINDOW_MS = 10 * 60 * 1000; // 10 minutes

const store = new Map<string, Trade[]>();

export function addTrade(trade: Trade): void {
  const symbol = trade.symbol;
  if (!store.has(symbol)) {
    store.set(symbol, []);
  }

  const trades = store.get(symbol)!;
  trades.push(trade);

  // Circular buffer: evict oldest when over capacity
  if (trades.length > MAX_TRADES_PER_SYMBOL) {
    trades.shift();
  }

  // Evict trades older than 10 minutes
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

export function getLastN(symbol: string, n: number): Trade[] {
  const trades = store.get(symbol);
  if (!trades || trades.length === 0) return [];
  return trades.slice(-n);
}

export function getSymbols(): string[] {
  return Array.from(store.keys());
}
