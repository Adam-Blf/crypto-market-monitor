export interface Metrics {
  symbol: string;
  timestamp: number;
  currentPrice: number;
  vwap: number;
  sma20: number;
  priceChange1m: number;
  priceChange5m: number;
  volumeTotal1m: number;
  tradeCount1m: number;
  highPrice1m: number;
  lowPrice1m: number;
  anomaly?: boolean;
  anomalyScore?: number;
}

export interface AnomalyEvent {
  symbol: string;
  timestamp: number;
  currentPrice: number;
  anomalyScore: number;
}

export type LangCode = 'fr' | 'en';
export type CryptoSymbol = 'BTC-USDT' | 'ETH-USDT' | 'BTC-USD' | 'SOL-USDT' | 'BNB-USDT' | 'XRP-USDT';

export const SYMBOLS: CryptoSymbol[] = ['BTC-USDT', 'ETH-USDT', 'BTC-USD', 'SOL-USDT', 'BNB-USDT', 'XRP-USDT'];

export interface AlertConfig {
  symbol: CryptoSymbol;
  priceAbove?: number;
  priceBelow?: number;
  zscoreAbove?: number;
  enabled: boolean;
}
export const MAX_CHART_POINTS = 100;
export const MAX_ANOMALIES = 50;
export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:3001';
