export interface Trade {
  exchange: 'binance' | 'coinbase';
  symbol: string;
  price: number;
  quantity: number;
  timestamp: number;
  tradeId: string;
  side: 'buy' | 'sell' | 'unknown';
  value: number;
}

export interface Metrics {
  symbol: string;
  timestamp: number;
  vwap: number;
  sma20: number;
  currentPrice: number;
  priceChange1m: number;
  priceChange5m: number;
  volumeTotal1m: number;
  tradeCount1m: number;
  anomaly: boolean;
  anomalyScore: number;
  highPrice1m: number;
  lowPrice1m: number;
}

export interface StoreEntry {
  trades: Trade[];
  lastEvicted: number;
}
