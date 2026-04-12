document.addEventListener('DOMContentLoaded', function() {
  // Create loader HTML
  var loader = document.createElement('div');
  loader.id = 'ev-loader';
  loader.innerHTML = `
    <div id="ev-particles" style="position:absolute;width:100%;height:100%;overflow:hidden;top:0;left:0;pointer-events:none;"></div>
    <div class="ev-loader-title">⚡ EV CHARGE HUB</div>
    <div class="ev-loader-subtitle">Smart Charging · Smarter Living</div>
    <div class="road-container">
      <span class="lightning lightning-1">⚡</span>
      <span class="lightning lightning-2">⚡</span>
      <span class="lightning lightning-3">⚡</span>
      <div class="ev-car">🚗</div>
      <div class="road">
        <div class="road-line"></div>
        <div class="road-line"></div>
        <div class="road-line"></div>
        <div class="road-line"></div>
      </div>
    </div>
    <div class="ev-progress-container"><div class="ev-progress-bar"></div></div>
    <div class="ev-progress-text">CHARGING YOUR EXPERIENCE...</div>
  `;
  document.body.insertBefore(loader, document.body.firstChild);

  // Add particles
  var pc = document.getElementById('ev-particles');
  for(var i = 0; i < 20; i++) {
    var p = document.createElement('div');
    p.className = 'ev-particle';
    p.style.left = Math.random() * 100 + '%';
    p.style.animationDuration = (Math.random() * 3 + 2) + 's';
    p.style.animationDelay = (Math.random() * 2) + 's';
    p.style.width = p.style.height = (Math.random() * 4 + 2) + 'px';
    pc.appendChild(p);
  }

  // Hide after 2.5 seconds
  setTimeout(function() {
    var l = document.getElementById('ev-loader');
    if(l) l.classList.add('hidden');
  }, 2500);
});
