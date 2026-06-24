import WebSocket from 'ws';
import { Trade, BinanceTradeEvent } from './types';
import { sendTrade } from './producer';

const BINANCE_WS_URL =
  'wss://stream.binance.com:9443/stream?streams=btcusdt@trade/ethusdt@trade';

const MAX_RETRIES = 10;
const BASE_DELAY_MS = 1_000;

const SYMBOL_MAP: Record<string, string> = {
  BTCUSDT: 'BTC-USDT',
  ETHUSDT: 'ETH-USDT',
};

let tradeCount = 0;

function normalizeSymbol(raw: string): string {
  return SYMBOL_MAP[raw.toUpperCase()] ?? raw.toUpperCase();
}

function parseBinanceTrade(event: BinanceTradeEvent): Trade {
  const price = parseFloat(event.p);
  const quantity = parseFloat(event.q);
  return {
    exchange: 'binance',
    symbol: normalizeSymbol(event.s),
    price,
    quantity,
    timestamp: event.T,
    tradeId: `binance-${event.t}`,
    side: event.m ? 'sell' : 'buy',
    value: price * quantity,
  };
}

export function startBinanceClient(retries = 0): void {
  console.log(`[binance] connecting (attempt ${retries + 1}/${MAX_RETRIES})...`);

  const ws = new WebSocket(BINANCE_WS_URL);

  const statsInterval = setInterval(() => {
    console.log(`[binance] trades ingested: ${tradeCount}`);
  }, 30_000);

  ws.on('open', () => {
    console.log('[binance] connected to stream');
    retries = 0;
  });

  ws.on('message', async (data: WebSocket.RawData) => {
    try {
      const msg = JSON.parse(data.toString()) as { data: BinanceTradeEvent };
      if (msg.data?.e === 'trade') {
        const trade = parseBinanceTrade(msg.data);
        await sendTrade(trade);
        tradeCount++;
      }
    } catch (err) {
      console.error('[binance] message parse error:', err);
    }
  });

  ws.on('close', (code, reason) => {
    clearInterval(statsInterval);
    console.warn(`[binance] connection closed (${code}): ${reason.toString()}`);
    scheduleReconnect(retries);
  });

  ws.on('error', (err) => {
    console.error('[binance] WebSocket error:', err.message);
    ws.terminate();
  });
}

function scheduleReconnect(retries: number): void {
  if (retries >= MAX_RETRIES) {
    console.error('[binance] max retries reached, giving up');
    return;
  }
  const delay = BASE_DELAY_MS * Math.pow(2, retries);
  console.log(`[binance] reconnecting in ${delay}ms...`);
  setTimeout(() => startBinanceClient(retries + 1), delay);
}
