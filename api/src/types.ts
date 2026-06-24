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

export interface ServerStats {
  connections: number;
  messagesPerSecond: number;
  uptime: number;
  timestamp: number;
}
