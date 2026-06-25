import type { AnomalyEvent } from '../types';
import { useI18n } from '../i18n';
import { formatPrice, formatTime } from '../utils';

interface Props {
  anomalies: AnomalyEvent[];
}

export function AnomalyFeed({ anomalies }: Props) {
  const { t, lang } = useI18n();

  return (
    <div className="anomaly-card card" role="region" aria-label="Flux d'anomalies">
      <div className="card-header">
        <span className="card-title">{t('anomaly.title')}</span>
        {anomalies.length > 0 && (
          <span className="anomaly-count-badge" aria-live="polite">
            {anomalies.length}
          </span>
        )}
      </div>
      <div className="anomaly-list" role="list">
        {anomalies.length === 0 ? (
          <p className="anomaly-empty">{t('anomaly.empty')}</p>
        ) : (
          anomalies.map((a, i) => (
            <div key={`${a.symbol}-${a.timestamp}-${i}`} className="anomaly-item" role="listitem">
              <div className="anomaly-item-header">
                <span className="anomaly-symbol">{a.symbol}</span>
                <span className="anomaly-time">{formatTime(a.timestamp, lang)}</span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 8 }}>
                <span className="anomaly-price">{formatPrice(a.currentPrice, lang)}</span>
                <span className="zscore-badge">z={a.anomalyScore.toFixed(2)}</span>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
