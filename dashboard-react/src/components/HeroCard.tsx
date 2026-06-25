import { useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import type { Metrics } from '../types';
import { useI18n } from '../i18n';
import { formatPrice, formatPct, formatTime } from '../utils';

interface Props {
  symbol: string;
  metrics: Metrics | undefined;
}

export function HeroCard({ symbol, metrics }: Props) {
  const { t, lang } = useI18n();
  const prevPriceRef = useRef<number | undefined>(undefined);
  const prevPrice = prevPriceRef.current;
  const priceDir = metrics && prevPrice != null
    ? metrics.currentPrice > prevPrice ? 'up' : metrics.currentPrice < prevPrice ? 'down' : null
    : null;

  useEffect(() => {
    if (metrics) prevPriceRef.current = metrics.currentPrice;
  }, [metrics?.currentPrice]); // eslint-disable-line react-hooks/exhaustive-deps

  const change1m = metrics?.priceChange1m ?? 0;
  const change5m = metrics?.priceChange5m ?? 0;

  return (
    <motion.section
      className="hero-card card"
      aria-label="Prix actuel et metriques principales"
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, ease: 'easeOut' }}
    >
      <div className="hero-left">
        <motion.div
          key={symbol}
          className="hero-symbol"
          initial={{ opacity: 0, x: -8 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.25 }}
        >
          {symbol}
        </motion.div>
        <AnimatePresence>
          <motion.div
            key={symbol}
            className={`hero-price ${priceDir === 'up' ? 'flash-up' : priceDir === 'down' ? 'flash-down' : ''}`}
            aria-live="polite"
            aria-label="Prix actuel"
            initial={{ opacity: 0.6, scale: 0.97 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.18 }}
          >
            {metrics ? formatPrice(metrics.currentPrice, lang) : '--,---.--'}
          </motion.div>
        </AnimatePresence>
        <div className="hero-change-row">
          <span className={`change-badge ${change1m >= 0 ? 'positive' : 'negative'}`}>{formatPct(change1m)}</span>
          <span className="change-label">{t('stats.change1m')}</span>
          <span className={`change-badge ${change5m >= 0 ? 'positive' : 'negative'}`}>{formatPct(change5m)}</span>
          <span className="change-label">{t('stats.change5m')}</span>
        </div>
      </div>
      <div className="hero-right">
        <div className="metric-item">
          <span className="metric-label">{t('price.vwap')}</span>
          <span className="metric-value">{metrics ? formatPrice(metrics.vwap, lang) : '-'}</span>
        </div>
        <div className="metric-item">
          <span className="metric-label">{t('price.sma20')}</span>
          <span className="metric-value">{metrics ? formatPrice(metrics.sma20, lang) : '-'}</span>
        </div>
        <div className="metric-item">
          <span className="metric-label">{t('price.lastUpdate')}</span>
          <span className="metric-value small">{metrics ? formatTime(metrics.timestamp, lang) : '-'}</span>
        </div>
      </div>
    </motion.section>
  );
}
