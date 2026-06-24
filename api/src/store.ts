import { Metrics } from './types';

const MAX_HISTORY = 200;
const MAX_ANOMALIES = 50;

const latestMetrics = new Map<string, Metrics>();
const historyMap = new Map<string, Metrics[]>();
const anomalies: Metrics[] = [];

export function updateMetrics(m: Metrics): void {
  latestMetrics.set(m.symbol, m);

  if (!historyMap.has(m.symbol)) {
    historyMap.set(m.symbol, []);
  }
  const history = historyMap.get(m.symbol)!;
  history.push(m);
  if (history.length > MAX_HISTORY) {
    history.shift();
  }

  if (m.anomaly) {
    anomalies.push(m);
    if (anomalies.length > MAX_ANOMALIES) {
      anomalies.shift();
    }
  }
}

export function getLatest(symbol?: string): Metrics | Record<string, Metrics> | null {
  if (symbol) {
    return latestMetrics.get(symbol.toUpperCase()) ?? null;
  }
  return Object.fromEntries(latestMetrics.entries());
}

export function getHistory(symbol: string, limit = 100): Metrics[] {
  const history = historyMap.get(symbol.toUpperCase()) ?? [];
  return history.slice(-Math.min(limit, MAX_HISTORY));
}

export function getAnomalies(limit = 20): Metrics[] {
  return anomalies.slice(-Math.min(limit, MAX_ANOMALIES));
}
