import WebSocket from 'ws';
import { Trade, CoinbaseTradeEvent } from './types';
import { sendTrade } from './producer';

const COINBASE_WS_URL = 'wss://advanced-trade-ws.coinbase.com';

const MAX_RETRIES = 10;
const BASE_DELAY_MS = 1_500;

const SUBSCRIBE_MSG = JSON.stringify({
  type: 'subscribe',
  channel: 'market_trades',
  product_ids: ['BTC-USD', 'ETH-USD'],
});

let tradeCount = 0;

function parseCoinbaseTrade(raw: {
  trade_id: string;
  product_id: string;
  price: string;
  size: string;
  side: string;
  time: string;
}): Trade {
  const price = parseFloat(raw.price);
  const quantity = parseFloat(raw.size);
  return {
    exchange: 'coinbase',
    symbol: raw.product_id,
    price,
    quantity,
    timestamp: new Date(raw.time).getTime(),
    tradeId: `coinbase-${raw.trade_id}`,
    side: raw.side === 'BUY' ? 'buy' : raw.side === 'SELL' ? 'sell' : 'unknown',
    value: price * quantity,
  };
}

export function startCoinbaseClient(retries = 0): void {
  console.log(`[coinbase] connecting (attempt ${retries + 1}/${MAX_RETRIES})...`);

  const ws = new WebSocket(COINBASE_WS_URL);

  const statsInterval = setInterval(() => {
    console.log(`[coinbase] trades ingested: ${tradeCount}`);
  }, 30_000);

  ws.on('open', () => {
    console.log('[coinbase] connected, subscribing to market_trades...');
    ws.send(SUBSCRIBE_MSG);
    retries = 0;
  });

  ws.on('message', async (data: WebSocket.RawData) => {
    try {
      const msg = JSON.parse(data.toString()) as CoinbaseTradeEvent;

      if (msg.type === 'error') {
        console.error('[coinbase] server error:', JSON.stringify(msg));
        return;
      }

      if (msg.channel === 'market_trades' && msg.events) {
        for (const event of msg.events) {
          if (event.type === 'update' && event.trades) {
            for (const rawTrade of event.trades) {
              const trade = parseCoinbaseTrade(rawTrade);
              await sendTrade(trade);
              tradeCount++;
            }
          }
        }
      }
    } catch (err) {
      console.error('[coinbase] message parse error:', err);
    }
  });

  ws.on('close', (code, reason) => {
    clearInterval(statsInterval);
    console.warn(`[coinbase] connection closed (${code}): ${reason.toString()}`);
    scheduleReconnect(retries);
  });

  ws.on('error', (err) => {
    console.error('[coinbase] WebSocket error:', err.message);
    ws.terminate();
  });
}

function scheduleReconnect(retries: number): void {
  if (retries >= MAX_RETRIES) {
    console.error('[coinbase] max retries reached, giving up');
    return;
  }
  const delay = BASE_DELAY_MS * Math.pow(2, retries);
  console.log(`[coinbase] reconnecting in ${delay}ms...`);
  setTimeout(() => startCoinbaseClient(retries + 1), delay);
}
