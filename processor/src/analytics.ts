import { Trade } from './types';

// VWAP = sum(prix * quantite) / sum(quantite) sur la fenetre 1min
// On utilise le VWAP plutot que le simple mean car il pondere par le volume reel
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

// SMA classique sur les N derniers trades (N=20 par defaut)
export function computeSMA(prices: number[]): number {
  if (prices.length === 0) return 0;
  return prices.reduce((sum, p) => sum + p, 0) / prices.length;
}

// Detection d'anomalie par z-score sur les quantites (pas les prix)
// Choix delibere: les spikes de volume sont plus predictifs que les spikes de prix
// seuil 2.5 sigma = ~1.2% des trades en dehors de la distribution normale
export function computeZScore(values: number[], current: number): number {
  if (values.length < 2) return 0;

  const mean = values.reduce((s, v) => s + v, 0) / values.length;
  const variance = values.reduce((s, v) => s + Math.pow(v - mean, 2), 0) / values.length;
  const std = Math.sqrt(variance);

  // Eviter la division par zero si tous les volumes sont identiques
  return std === 0 ? 0 : (current - mean) / std;
}

// Variation % par rapport au premier trade de la fenetre temporelle
// On garde le premier trade comme reference plutot que le close precedent
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

// Volume total = somme des quantites (en token, pas en USD)
export function computeVolume(trades: Trade[]): number {
  return trades.reduce((sum, t) => sum + t.quantity, 0);
}
