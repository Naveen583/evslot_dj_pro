// Dark/Light Mode Toggle - EV Charge Hub
(function() {
  // Create toggle button
  const btn = document.createElement('button');
  btn.id = 'theme-toggle';
  btn.innerHTML = '🌙';
  btn.title = 'Toggle Dark/Light Mode';
  btn.style.cssText = `
    position:fixed;bottom:90px;left:24px;width:44px;height:44px;
    border-radius:50%;border:none;cursor:pointer;z-index:9998;
    font-size:20px;box-shadow:0 4px 15px rgba(0,0,0,0.3);
    background:linear-gradient(135deg,#1a2a3a,#0d1117);
    transition:transform 0.2s;
  `;
  btn.onmouseover = () => btn.style.transform = 'scale(1.1)';
  btn.onmouseout = () => btn.style.transform = 'scale(1)';

  // Light mode CSS
  const lightStyle = document.createElement('style');
  lightStyle.id = 'light-mode-style';
  lightStyle.textContent = `
    body.light-mode { background:#f5f7fa !important; color:#333 !important; }
    body.light-mode .navbar { background:#fff !important; box-shadow:0 2px 10px rgba(0,0,0,0.1); }
    body.light-mode .navbar a { color:#333 !important; }
    body.light-mode .ftco-section { background:#f5f7fa !important; }
    body.light-mode .bg-light { background:#fff !important; }
    body.light-mode .contact-form { background:#fff !important; box-shadow:0 4px 20px rgba(0,0,0,0.1); }
    body.light-mode .form-control { background:#f8f9fa !important; border:1px solid #ddd !important; color:#333 !important; }
    body.light-mode .ftco-footer { background:#2c3e50 !important; }
    body.light-mode .hero-wrap { filter:brightness(0.9); }
    body.light-mode .border { border-color:#ddd !important; }
    body.light-mode p, body.light-mode h1, body.light-mode h2, body.light-mode h3, body.light-mode h4 { color:#333 !important; }
    body.light-mode .navbar-dark .navbar-nav .nav-link { color:#333 !important; }
    body.light-mode #theme-toggle { background:linear-gradient(135deg,#ffd700,#ff8c00) !important; }
  `;
  document.head.appendChild(lightStyle);

  // Apply saved theme
  const saved = localStorage.getItem('ev-theme');
  if (saved === 'light') {
    document.body.classList.add('light-mode');
    btn.innerHTML = '☀️';
  }

  btn.onclick = () => {
    document.body.classList.toggle('light-mode');
    const isLight = document.body.classList.contains('light-mode');
    btn.innerHTML = isLight ? '☀️' : '🌙';
    localStorage.setItem('ev-theme', isLight ? 'light' : 'dark');
  };

  document.body.appendChild(btn);
})();
