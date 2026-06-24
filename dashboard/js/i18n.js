'use strict';

const I18n = (() => {
  let _locale = localStorage.getItem('cmm-locale') || 'fr';
  let _translations = {};

  async function load(locale) {
    try {
      const res = await fetch(`i18n/${locale}.json`);
      if (!res.ok) throw new Error('Failed to load locale: ' + locale);
      _translations = await res.json();
      _locale = locale;
      localStorage.setItem('cmm-locale', locale);
      document.documentElement.lang = locale;
    } catch (err) {
      console.warn('[i18n] Could not load locale', locale, err);
    }
  }

  function t(key) {
    const keys = key.split('.');
    let val = _translations;
    for (const k of keys) {
      val = val?.[k];
    }
    return (val != null && typeof val === 'string') ? val : key;
  }

  function getLocale() {
    return _locale;
  }

  return { load, t, getLocale };
})();
