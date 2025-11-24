document.addEventListener('DOMContentLoaded', () => {
  const storageKey = 'zoo-theme';
  const root = document.documentElement;
  const toggle = document.getElementById('themeToggle');

  const applyTheme = (theme) => {
    const nextTheme = theme === 'dark' ? 'dark' : 'light';
    root.setAttribute('data-theme', nextTheme);
    if (toggle) {
      toggle.checked = nextTheme === 'dark';
    }
    try {
      localStorage.setItem(storageKey, nextTheme);
    } catch (err) {
      // LocalStorage might be unavailable (private mode), ignore silently.
    }
  };

  const initialTheme = (() => {
    if (root.getAttribute('data-theme')) {
      return root.getAttribute('data-theme');
    }
    try {
      return localStorage.getItem(storageKey) || 'dark';
    } catch (err) {
      return 'dark';
    }
  })();

  applyTheme(initialTheme);

  if (toggle) {
    toggle.addEventListener('change', () => {
      applyTheme(toggle.checked ? 'dark' : 'light');
    });
  }
});

