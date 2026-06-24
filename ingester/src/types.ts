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

export interface KafkaConfig {
  brokers: string[];
  topic: string;
  clientId: string;
}

export interface BinanceTradeEvent {
  e: string;
  E: number;
  s: string;
  t: number;
  p: string;
  q: string;
  b: number;
  a: number;
  T: number;
  m: boolean;
}

export interface CoinbaseTradeEvent {
  type: string;
  channel: string;
  events: CoinbaseTradeEventItem[];
}

export interface CoinbaseTradeEventItem {
  type: string;
  trades: CoinbaseTrade[];
}

export interface CoinbaseTrade {
  trade_id: string;
  product_id: string;
  price: string;
  size: string;
  side: string;
  time: string;
}
