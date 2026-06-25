import type { LangCode } from '../types';
import { useI18n } from '../i18n';
import { useClock } from '../hooks/useClock';

interface Props {
  connected: boolean;
  demoMode: boolean;
}

export function Header({ connected, demoMode }: Props) {
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
            <div className="logo-subtitle">M1 EFREI - Real-Time Engineering</div>
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
