import WebSocket from 'ws';
import { Trade, BinanceTradeEvent } from './types';
import { sendTrade } from './producer';

// Stream combiné Binance: une seule connexion WS pour toutes les paires
// Format: <symbol>@trade - latence typique < 50ms depuis les serveurs EU
const BINANCE_WS_URL =
  'wss://stream.binance.com:9443/stream?streams=btcusdt@trade/ethusdt@trade/solusdt@trade/bnbusdt@trade/xrpusdt@trade';

const MAX_RETRIES = 10;
const BASE_DELAY_MS = 1_000;

// Mapping symbole Binance -> format normalise du pipeline
const SYMBOL_MAP: Record<string, string> = {
  BTCUSDT: 'BTC-USDT',
  ETHUSDT: 'ETH-USDT',
  SOLUSDT: 'SOL-USDT',
  BNBUSDT: 'BNB-USDT',
  XRPUSDT: 'XRP-USDT',
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
    // event.m = true si le buyer est market maker (donc le seller est agresseur)
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

// Reconnexion exponentielle avec jitter implicite via les delais d'execution Node
function scheduleReconnect(retries: number): void {
  if (retries >= MAX_RETRIES) {
    console.error('[binance] max retries reached, giving up');
    return;
  }
  const delay = BASE_DELAY_MS * Math.pow(2, retries);
  console.log(`[binance] reconnecting in ${delay}ms...`);
  setTimeout(() => startBinanceClient(retries + 1), delay);
}
