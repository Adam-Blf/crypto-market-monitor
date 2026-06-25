import { useRef, useEffect } from 'react';
import type { Metrics } from '../types';
import { useI18n } from '../i18n';
import { formatPrice, formatPct, formatTime } from '../utils';

interface Props {
  symbol: string;
  metrics: Metrics | undefined;
}

export function HeroCard({ symbol, metrics }: Props) {
  const { t, lang } = useI18n();
  const priceRef = useRef<HTMLDivElement>(null);
  const prevPriceRef = useRef<number | undefined>(undefined);

  useEffect(() => {
    if (!metrics || !priceRef.current) return;
    const prev = prevPriceRef.current;
    if (prev != null && prev !== metrics.currentPrice) {
      const cls = metrics.currentPrice > prev ? 'flash-up' : 'flash-down';
      const el = priceRef.current;
      el.classList.remove('flash-up', 'flash-down');
      void el.offsetWidth; // reflow
      el.classList.add(cls);
    }
    prevPriceRef.current = metrics.currentPrice;
  }, [metrics?.currentPrice]); // eslint-disable-line react-hooks/exhaustive-deps

  const change1m = metrics?.priceChange1m ?? 0;
  const change5m = metrics?.priceChange5m ?? 0;

  return (
    <section className="hero-card card" aria-label="Prix actuel et metriques principales">
      <div className="hero-left">
        <div className="hero-symbol">{symbol}</div>
        <div className="hero-price" ref={priceRef} aria-live="polite" aria-label="Prix actuel">
          {metrics ? formatPrice(metrics.currentPrice, lang) : '--,---.--'}
        </div>
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
    </section>
  );
}
