import { motion } from 'framer-motion';
import type { LangCode } from '../types';
import { useI18n } from '../i18n';
import { useClock } from '../hooks/useClock';

interface Props {
  connected: boolean;
  demoMode: boolean;
  alertCount: number;
  onAlertsClick: () => void;
}

export function Header({ connected, demoMode, alertCount, onAlertsClick }: Props) {
  const { t, lang, setLang } = useI18n();
  const time = useClock(lang);

  return (
    <header className="header" role="banner">
      <div className="header-left">
        <div className="logo" aria-label="Crypto Monitor">
          <svg className="logo-icon" width="20" height="20" viewBox="0 0 20 20" fill="none" aria-hidden="true">
            <path d="M10 2L17.32 6V14L10 18L2.68 14V6L10 2Z" stroke="#F59E0B" strokeWidth="1.5" fill="rgba(245,158,11,0.08)" />
            <circle cx="10" cy="10" r="2.5" fill="#F59E0B" />
          </svg>
          <div>
            <div className="logo-text">{t('title')}</div>
            <div className="logo-subtitle">Real-Time Data Pipeline</div>
          </div>
        </div>
        {demoMode ? (
          <div className="header-badge" style={{ background: 'rgba(245,158,11,0.15)', color: '#F59E0B', borderColor: 'rgba(245,158,11,0.3)', animation: 'none' }}>
            DEMO
          </div>
        ) : (
          <div className="header-badge">{t('live')}</div>
        )}
      </div>

      <div className="header-center">
        <time className="clock" aria-label="Heure actuelle">{time}</time>
      </div>

      <div className="header-right" style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        <button
          className="alert-bell-btn"
          onClick={onAlertsClick}
          aria-label={`Alertes${alertCount > 0 ? ` (${alertCount} actives)` : ''}`}
          title="Configurer les alertes prix"
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>
            <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
          </svg>
          {alertCount > 0 && (
            <motion.span
              className="alert-bell-count"
              key={alertCount}
              initial={{ scale: 1.5 }}
              animate={{ scale: 1 }}
              transition={{ type: 'spring', stiffness: 500, damping: 20 }}
            >
              {alertCount}
            </motion.span>
          )}
        </button>

        <div className="connection-status" role="status" aria-live="polite">
          <span className={`status-dot${connected ? ' connected' : ''}`} aria-hidden="true" />
          <span className="status-label">{connected ? t('connected') : t('disconnected')}</span>
        </div>
        <div className="lang-switcher" role="group" aria-label="Choix de la langue">
          {(['fr', 'en'] as LangCode[]).map((l, i) => (
            <>
              {i > 0 && <span className="lang-sep" aria-hidden="true">|</span>}
              <button
                key={l}
                className={`lang-btn${lang === l ? ' active' : ''}`}
                onClick={() => setLang(l)}
                aria-pressed={lang === l}
              >
                {l.toUpperCase()}
              </button>
            </>
          ))}
        </div>
      </div>
    </header>
  );
}
