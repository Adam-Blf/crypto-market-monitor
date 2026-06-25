export function formatPrice(n: number | null | undefined, lang = 'fr'): string {
  if (n == null || isNaN(n)) return '-';
  const locale = lang === 'fr' ? 'fr-FR' : 'en-US';
  return n.toLocaleString(locale, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

export function formatVolume(n: number | null | undefined): string {
  if (n == null || isNaN(n)) return '-';
  if (n >= 1_000_000) return (n / 1_000_000).toFixed(2) + 'M';
  if (n >= 1_000) return (n / 1_000).toFixed(2) + 'K';
  return n.toFixed(2);
}

export function formatPct(n: number | null | undefined): string {
  if (n == null || isNaN(n)) return '0.00%';
  const sign = n >= 0 ? '+' : '';
  return sign + n.toFixed(2) + '%';
}

export function formatTime(ts: number, lang = 'fr'): string {
  const locale = lang === 'fr' ? 'fr-FR' : 'en-US';
  return new Date(ts).toLocaleTimeString(locale, { hour12: false });
}

export function playAnomalyBeep(): void {
  try {
    const AudioCtx = window.AudioContext || (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext;
    const ac = new AudioCtx();
    const osc = ac.createOscillator();
    const gain = ac.createGain();
    osc.connect(gain);
    gain.connect(ac.destination);
    osc.frequency.value = 880;
    osc.type = 'sine';
    gain.gain.setValueAtTime(0.08, ac.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, ac.currentTime + 0.25);
    osc.start();
    osc.stop(ac.currentTime + 0.25);
  } catch (_) { /* AudioContext unavailable */ }
}
