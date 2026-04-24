// Full Page Tamil/English Language Toggle - EV Charge Hub
(function() {
  let currentLang = localStorage.getItem('ev-page-lang') || 'ta';

  const translations = {
    'Home': 'முகப்பு',
    'Station': 'நிலையம்',
    'Tariff': 'கட்டணம்',
    'History': 'வரலாறு',
    'Logout': 'வெளியேறு',
    'User': 'பயனர்',
    'Admin': 'நிர்வாகி',
    'Charging Station': 'சார்ஜிங் நிலையம்',
    'Login': 'உள்நுழை',
    'Register': 'பதிவு செய்',
    'Submit': 'சமர்ப்பி',
    'Username': 'பயனர்பெயர்',
    'Password': 'கடவுச்சொல்',
    'Email': 'மின்னஞ்சல்',
    'Mobile': 'மொபைல்',
    'Name': 'பெயர்',
    'Address': 'முகவரி',
    'Book Slot': 'ஸ்லாட் புக் செய்',
    'OUT': 'வெளியேறு',
    'Reschedule': 'மறுதிட்டமிடு',
    'Need Charge': 'சார்ஜ் வேண்டும்',
    'Charge Completed': 'சார்ஜ் முடிந்தது',
    'Payment': 'கட்டணம்',
    'Booking': 'முன்பதிவு',
    'Slot': 'ஸ்லாட்',
    'Available': 'கிடைக்கும்',
    'Booked': 'முன்பதிவு செய்யப்பட்டது',
    'Cancel': 'ரத்து செய்',
    'Confirm': 'உறுதிப்படுத்து',
    'Back': 'திரும்பு',
    'Next': 'அடுத்து',
    'Save': 'சேமி',
    'Update': 'புதுப்பி',
    'Delete': 'நீக்கு',
    'Search': 'தேடு',
    'View': 'பார்',
    'Download': 'பதிவிறக்கு',
    'Print': 'அச்சிடு',
    'Report': 'அறிக்கை',
    'Dashboard': 'டாஷ்போர்டு',
    'Profile': 'சுயவிவரம்',
    'Settings': 'அமைப்புகள்',
    'Forgot Password?': 'கடவுச்சொல் மறந்தீர்களா?',
    'New Station ?': 'புதிய நிலையமா?',
    'Register here': 'இங்கே பதிவு செய்யுங்கள்',
    'Vehicle No': 'வாகன எண்',
    'Date': 'தேதி',
    'Time': 'நேரம்',
    'Amount': 'தொகை',
    'Status': 'நிலை',
    'Action': 'செயல்',
    'Total': 'மொத்தம்',
    'Wait Room': 'காத்திருப்பு அறை',
    'QR Code': 'QR குறியீடு',
    'Charging Station Login': 'சார்ஜிங் நிலையம் உள்நுழைவு',
    'Charging Station Home': 'சார்ஜிங் நிலையம் முகப்பு',
    'Charging Plan Selection': 'சார்ஜிங் திட்டம் தேர்வு',
    'Booking Confirmed': 'முன்பதிவு உறுதிப்படுத்தப்பட்டது',
    'Select Your Plan': 'உங்கள் திட்டத்தை தேர்வு செய்யுங்கள்',
    'For Login': 'உள்நுழைவுக்கு',
    'Station Details': 'நிலையம் விவரங்கள்',
    'View': 'பார்க்க',
    'Reports': 'அறிக்கைகள்',
    'Home': 'முகப்பு',
  };

  const langBtn = document.createElement('button');
  langBtn.id = 'page-lang-btn';
  langBtn.style.cssText = `
    position:fixed;top:70px;right:16px;z-index:9997;
    background:linear-gradient(135deg,#0072ff,#7b2ff7);
    color:#fff;border:none;border-radius:20px;
    padding:8px 16px;font-size:13px;font-weight:700;
    cursor:pointer;box-shadow:0 2px 10px rgba(0,114,255,0.4);
    font-family:'Poppins',sans-serif;letter-spacing:1px;
    transition:transform 0.2s;
  `;
  langBtn.onmouseover = () => langBtn.style.transform = 'scale(1.05)';
  langBtn.onmouseout = () => langBtn.style.transform = 'scale(1)';

  function updateBtn() {
    langBtn.textContent = currentLang === 'ta' ? '🌐 English' : '🌐 தமிழ்';
  }

  function translatePage(toLang) {
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    const nodes = [];
    while (walker.nextNode()) {
      const node = walker.currentNode;
      if (node.parentElement && !['SCRIPT','STYLE','INPUT','TEXTAREA','BUTTON'].includes(node.parentElement.tagName)) {
        nodes.push(node);
      }
    }

    if (toLang === 'ta') {
      nodes.forEach(node => {
        const trimmed = node.textContent.trim();
        if (translations[trimmed]) {
          node.textContent = node.textContent.replace(trimmed, translations[trimmed]);
        }
      });
    } else {
      const reverse = {};
      Object.entries(translations).forEach(([en, ta]) => reverse[ta] = en);
      nodes.forEach(node => {
        const trimmed = node.textContent.trim();
        if (reverse[trimmed]) {
          node.textContent = node.textContent.replace(trimmed, reverse[trimmed]);
        }
      });
    }
  }

  langBtn.onclick = () => {
    currentLang = currentLang === 'ta' ? 'en' : 'ta';
    localStorage.setItem('ev-page-lang', currentLang);
    translatePage(currentLang);
    updateBtn();
  };

  window.addEventListener('load', () => {
    if (currentLang === 'ta') translatePage('ta');
    updateBtn();
  });

  document.body.appendChild(langBtn);
})();

  const translations = {
    // Navigation
    'Home': 'முகப்பு',
    'Station': 'நிலையம்',
    'Tariff': 'கட்டணம்',
    'History': 'வரலாறு',
    'Logout': 'வெளியேறு',
    'User': 'பயனர்',
    'Admin': 'நிர்வாகி',
    'Charging Station': 'சார்ஜிங் நிலையம்',
    // Common
    'Login': 'உள்நுழை',
    'Register': 'பதிவு செய்',
    'Submit': 'சமர்ப்பி',
    'Username': 'பயனர்பெயர்',
    'Password': 'கடவுச்சொல்',
    'Email': 'மின்னஞ்சல்',
    'Mobile': 'மொபைல்',
    'Name': 'பெயர்',
    'Address': 'முகவரி',
    'Book Slot': 'ஸ்லாட் புக் செய்',
    'OUT': 'வெளியேறு',
    'Reschedule': 'மறுதிட்டமிடு',
    'Need Charge': 'சார்ஜ் வேண்டும்',
    'Charge Completed': 'சார்ஜ் முடிந்தது',
    'Payment': 'கட்டணம்',
    'Booking': 'முன்பதிவு',
    'Slot': 'ஸ்லாட்',
    'Available': 'கிடைக்கும்',
    'Booked': 'முன்பதிவு செய்யப்பட்டது',
    'Cancel': 'ரத்து செய்',
    'Confirm': 'உறுதிப்படுத்து',
    'Back': 'திரும்பு',
    'Next': 'அடுத்து',
    'Save': 'சேமி',
    'Update': 'புதுப்பி',
    'Delete': 'நீக்கு',
    'Search': 'தேடு',
    'View': 'பார்',
    'Download': 'பதிவிறக்கு',
    'Print': 'அச்சிடு',
    'Report': 'அறிக்கை',
    'Dashboard': 'டாஷ்போர்டு',
    'Profile': 'சுயவிவரம்',
    'Settings': 'அமைப்புகள்',
    'Forgot Password?': 'கடவுச்சொல் மறந்தீர்களா?',
    'New Station ?': 'புதிய நிலையமா?',
    'Register here': 'இங்கே பதிவு செய்யுங்கள்',
    'Vehicle No': 'வாகன எண்',
    'Date': 'தேதி',
    'Time': 'நேரம்',
    'Amount': 'தொகை',
    'Status': 'நிலை',
    'Action': 'செயல்',
    'Total': 'மொத்தம்',
    'Level 1': 'நிலை 1',
    'Level 2': 'நிலை 2',
    'DC Fast': 'DC வேகம்',
    'Wait Room': 'காத்திருப்பு அறை',
    'QR Code': 'QR குறியீடு',
  };

  // Create language toggle button
  const langBtn = document.createElement('button');
  langBtn.id = 'page-lang-btn';
  langBtn.style.cssText = `
    position:fixed;top:70px;right:16px;z-index:9997;
    background:linear-gradient(135deg,#0072ff,#7b2ff7);
    color:#fff;border:none;border-radius:20px;
    padding:6px 14px;font-size:12px;font-weight:700;
    cursor:pointer;box-shadow:0 2px 10px rgba(0,114,255,0.4);
    font-family:'Poppins',sans-serif;letter-spacing:1px;
    transition:transform 0.2s;
  `;
  langBtn.onmouseover = () => langBtn.style.transform = 'scale(1.05)';
  langBtn.onmouseout = () => langBtn.style.transform = 'scale(1)';

  function updateBtn() {
    langBtn.textContent = currentLang === 'en' ? '🌐 தமிழ்' : '🌐 English';
  }

  function translatePage(toLang) {
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    const nodes = [];
    while (walker.nextNode()) {
      const node = walker.currentNode;
      if (node.parentElement && !['SCRIPT','STYLE','INPUT','TEXTAREA'].includes(node.parentElement.tagName)) {
        nodes.push(node);
      }
    }

    if (toLang === 'ta') {
      nodes.forEach(node => {
        const trimmed = node.textContent.trim();
        if (translations[trimmed]) {
          node.textContent = node.textContent.replace(trimmed, translations[trimmed]);
        }
      });
    } else {
      // Reverse translate
      const reverse = {};
      Object.entries(translations).forEach(([en, ta]) => reverse[ta] = en);
      nodes.forEach(node => {
        const trimmed = node.textContent.trim();
        if (reverse[trimmed]) {
          node.textContent = node.textContent.replace(trimmed, reverse[trimmed]);
        }
      });
    }
  }

  langBtn.onclick = () => {
    currentLang = currentLang === 'en' ? 'ta' : 'en';
    localStorage.setItem('ev-page-lang', currentLang);
    translatePage(currentLang);
    updateBtn();
  };

  // Apply saved language on load
  window.addEventListener('load', () => {
    if (currentLang === 'ta') translatePage('ta');
    updateBtn();
  });

  document.body.appendChild(langBtn);
})(); 
