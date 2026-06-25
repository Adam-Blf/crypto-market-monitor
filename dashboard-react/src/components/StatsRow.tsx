import type { Metrics } from '../types';
import { useI18n } from '../i18n';
import { formatPrice, formatVolume } from '../utils';

interface Props {
  metrics: Metrics | undefined;
}

export function StatsRow({ metrics }: Props) {
  const { t, lang } = useI18n();

  return (
    <div className="stats-row" role="region" aria-label="Statistiques du marche">
      <div className="stat-card card">
        <div className="stat-label">{t('stats.volume')}</div>
        <div className="stat-value">{formatVolume(metrics?.volumeTotal1m)}</div>
      </div>
      <div className="stat-card card">
        <div className="stat-label">{t('stats.trades')}</div>
        <div className="stat-value">{metrics?.tradeCount1m ?? '-'}</div>
      </div>
      <div className="stat-card card">
        <div className="stat-label">{t('stats.high')}</div>
        <div className="stat-value positive">{formatPrice(metrics?.highPrice1m, lang)}</div>
      </div>
      <div className="stat-card card">
        <div className="stat-label">{t('stats.low')}</div>
        <div className="stat-value negative">{formatPrice(metrics?.lowPrice1m, lang)}</div>
      </div>
    </div>
  );
}
