import { motion, AnimatePresence } from 'framer-motion';
import type { Metrics } from '../types';
import { useI18n } from '../i18n';
import { formatPrice } from '../utils';

interface Props {
  metrics: Record<string, Metrics>;
}

// Widget spread Binance/Coinbase: montre l'ecart de prix BTC entre les deux exchanges
// En theorie BTC-USDT et BTC-USD devraient etre quasi-identiques (arbitrage rapide)
// Un spread persistant > 0.1% peut indiquer une friction de liquidite ou un lag de prix
export function SpreadWidget({ metrics }: Props) {
  const { lang } = useI18n();

  const binance = metrics['BTC-USDT'];
  const coinbase = metrics['BTC-USD'];

  if (!binance || !coinbase) {
    return (
      <div className="spread-widget card">
        <div className="card-header">
          <span className="card-title">BTC Spread · Binance / Coinbase</span>
        </div>
        <p className="anomaly-empty">En attente de donnees...</p>
      </div>
    );
  }

  const spread = binance.currentPrice - coinbase.currentPrice;
  const spreadPct = (spread / coinbase.currentPrice) * 100;
  const isPositive = spread >= 0;

  // Flèche directionnelle: neutre si < 0.5$ d'ecart (bruit de marche)
  const arrow = spread > 0.5 ? '▲' : spread < -0.5 ? '▼' : '≈';
  const color = Math.abs(spreadPct) > 0.1
    ? (isPositive ? 'var(--price-up)' : 'var(--price-down)')
    : 'var(--text-secondary)';

  return (
    <div className="spread-widget card">
      <div className="card-header">
        <span className="card-title">BTC Spread · Binance / Coinbase</span>
        <span className="card-subtitle" style={{ color: 'var(--text-muted)', fontSize: 11 }}>temps reel</span>
      </div>
      <div className="spread-body">
        <div className="spread-exchange-row">
          <div className="spread-exchange">
            <img src="/icons/bitcoin.svg" width={16} height={16} alt="" aria-hidden="true" />
            <span className="spread-exchange-name">Binance</span>
            <span className="spread-price">{formatPrice(binance.currentPrice, lang)}</span>
          </div>
          <div className="spread-exchange">
            <img src="/icons/coinbase.svg" width={16} height={16} alt="" aria-hidden="true" />
            <span className="spread-exchange-name">Coinbase</span>
            <span className="spread-price">{formatPrice(coinbase.currentPrice, lang)}</span>
          </div>
        </div>
        <div className="spread-result-row">
          <AnimatePresence>
            <motion.div
              key={Math.round(spread * 100)}
              className="spread-value"
              style={{ color }}
              initial={{ opacity: 0.5, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.2 }}
            >
              <span className="spread-arrow">{arrow}</span>
              <span>{isPositive ? '+' : ''}{fmt(spread)} $</span>
              <span className="spread-pct">({isPositive ? '+' : ''}{spreadPct.toFixed(4)}%)</span>
            </motion.div>
          </AnimatePresence>
          <span className="spread-label">ecart de prix</span>
        </div>
      </div>
    </div>
  );
}
