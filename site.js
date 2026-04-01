// ── NAVBAR MOBILE TOGGLE ──
const toggle = document.querySelector('.nav-toggle');
const navLinks = document.querySelector('.nav-links');
if (toggle && navLinks) {
  toggle.onclick = null; // rimuovi onclick inline se presente
  toggle.addEventListener('click', () => {
    navLinks.classList.toggle('open');
  });
}

// ── CHIUDI NAVBAR MOBILE AL CLICK SUI LINK ──
if (navLinks) {
  navLinks.querySelectorAll('a').forEach(a => {
    a.addEventListener('click', () => navLinks.classList.remove('open'));
  });
}

// ── ACTIVE NAV LINK — compatibile file:// ──
(function () {
  const path = location.pathname;
  const current = path.substring(path.lastIndexOf('/') + 1) || 'index.html';
  document.querySelectorAll('.nav-links > a').forEach(a => {
    const href = (a.getAttribute('href') || '').split('#')[0];
    if (href === current) a.classList.add('active');
  });
  // evidenzia anche la voce Approfondimenti se siamo su doc-*
  if (current.startsWith('doc-') || current === 'approfondimenti.html') {
    document.querySelectorAll('.nav-dropdown > a').forEach(a => {
      if ((a.getAttribute('href') || '').includes('approfondimenti')) a.classList.add('active');
    });
  }
})();

// ── ACCORDION ──
document.querySelectorAll('.accordion-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const body = btn.nextElementSibling;
    const isOpen = body.classList.contains('open');
    document.querySelectorAll('.accordion-body').forEach(b => b.classList.remove('open'));
    document.querySelectorAll('.accordion-btn').forEach(b => b.classList.remove('open'));
    if (!isOpen) { body.classList.add('open'); btn.classList.add('open'); }
  });
});

// ── DROPDOWN TOUCH (mobile/tablet) ──
document.querySelectorAll('.nav-dropdown').forEach(dd => {
  const menu = dd.querySelector('.nav-dropdown-menu');
  const link = dd.querySelector('a');
  if (!menu || !link) return;
  const isTouch = ('ontouchstart' in window) || navigator.maxTouchPoints > 0;
  if (isTouch) {
    link.addEventListener('click', e => {
      const visible = menu.style.display === 'block';
      document.querySelectorAll('.nav-dropdown-menu').forEach(m => m.style.display = 'none');
      if (!visible) { e.preventDefault(); menu.style.display = 'block'; }
    });
    document.addEventListener('click', e => {
      if (!dd.contains(e.target)) menu.style.display = 'none';
    });
  }
});

// ── FIX ANCHOR SCROLL su file:// ──
// Chrome blocca scroll-behavior:smooth su file://, forziamo JS
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const id = a.getAttribute('href').slice(1);
    if (!id) return;
    const target = document.getElementById(id);
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});
