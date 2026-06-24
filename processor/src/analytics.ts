import { Trade } from './types';

export function computeVWAP(trades: Trade[]): number {
  if (trades.length === 0) return 0;

  let totalValue = 0;
  let totalVolume = 0;

  for (const t of trades) {
    totalValue += t.price * t.quantity;
    totalVolume += t.quantity;
  }

  return totalVolume === 0 ? 0 : totalValue / totalVolume;
}

export function computeSMA(prices: number[]): number {
  if (prices.length === 0) return 0;
  return prices.reduce((sum, p) => sum + p, 0) / prices.length;
}

export function computeZScore(values: number[], current: number): number {
  if (values.length < 2) return 0;

  const mean = values.reduce((s, v) => s + v, 0) / values.length;
  const variance = values.reduce((s, v) => s + Math.pow(v - mean, 2), 0) / values.length;
  const std = Math.sqrt(variance);

  return std === 0 ? 0 : (current - mean) / std;
}

export function computePriceChange(
  currentPrice: number,
  pastTrades: Trade[],
  windowMs: number
): number {
  if (pastTrades.length === 0) return 0;

  const cutoff = Date.now() - windowMs;
  const windowTrades = pastTrades.filter((t) => t.timestamp >= cutoff);

  if (windowTrades.length === 0) return 0;

  const referencePrice = windowTrades[0].price;
  return referencePrice === 0 ? 0 : ((currentPrice - referencePrice) / referencePrice) * 100;
}

export function computeHighLow(trades: Trade[]): { high: number; low: number } {
  if (trades.length === 0) return { high: 0, low: 0 };

  let high = trades[0].price;
  let low = trades[0].price;

  for (const t of trades) {
    if (t.price > high) high = t.price;
    if (t.price < low) low = t.price;
  }

  return { high, low };
}

export function computeVolume(trades: Trade[]): number {
  return trades.reduce((sum, t) => sum + t.quantity, 0);
}
