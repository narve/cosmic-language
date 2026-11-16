// Adds a small button that switches symbol names between words and logic
// symbols by toggling the --use-logical-symbols CSS variable (see style.css).
(() => {
  const root = document.documentElement;
  const storageKey = 'use-logical-symbols';
  const button = document.createElement('button');
  button.type = 'button';
  button.dataset.toggle = 'logical-symbols';
  button.textContent = '¬ ∧ ∨';
  button.title = 'Show logic symbols instead of words';
  button.setAttribute('aria-label', 'Logic symbols');

  const apply = on => {
    root.style.setProperty('--use-logical-symbols', on ? '1' : '0');
    button.setAttribute('aria-pressed', String(on));
  };

  let on = false;
  try { on = localStorage.getItem(storageKey) === '1'; } catch {}
  apply(on);

  button.addEventListener('click', () => {
    on = !on;
    apply(on);
    try { localStorage.setItem(storageKey, on ? '1' : '0'); } catch {}
  });
  document.body.append(button);
})();
