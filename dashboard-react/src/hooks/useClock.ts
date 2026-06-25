import { useState, useEffect } from 'react';

export function useClock(lang: string): string {
  const [time, setTime] = useState('');

  useEffect(() => {
    const locale = lang === 'fr' ? 'fr-FR' : 'en-US';
    const tick = () => setTime(new Date().toLocaleTimeString(locale, { hour12: false }));
    tick();
    const id = setInterval(tick, 1000);
    return () => clearInterval(id);
  }, [lang]);

  return time;
}
