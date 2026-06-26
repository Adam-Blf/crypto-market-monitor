import { useI18n } from '../i18n';

interface Props {
  serverStats: string;
  msgCount: number;
  demoMode: boolean;
}

export function Footer({ serverStats, msgCount, demoMode }: Props) {
  const { t } = useI18n();

  return (
    <footer className="footer" role="contentinfo">
      <span>Crypto Market Monitor</span>
      <span className="footer-dot">·</span>
      <span>M1 EFREI - Real-Time Engineering</span>
      <span className="footer-dot">·</span>
      <span>Apache Kafka 3.7 + Socket.IO</span>
      <span className="footer-dot">·</span>
      {demoMode ? (
        <span style={{ color: '#F59E0B' }}>{t('footer.demo')}</span>
      ) : (
        <span>{serverStats}</span>
      )}
      <span className="footer-dot">·</span>
      <span>{msgCount.toLocaleString()} {t('footer.messages')}</span>
    </footer>
  );
}
