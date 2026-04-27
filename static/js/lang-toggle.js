// Custom Multi-Language Dropdown using Google Translate (Hidden)
(function() {

    // 1. Inject hidden Google Translate element
    const gtContainer = document.createElement('div');
    gtContainer.id = 'google_translate_element';
    gtContainer.style.display = 'none';
    document.body.appendChild(gtContainer);

    // 2. Load Google Translate Script
    window.googleTranslateElementInit = function() {
        new google.translate.TranslateElement({
            pageLanguage: 'en',
            includedLanguages: 'en,ta,hi,ml,te,kn,bn,gu,mr,ur', // Major Indian languages
            layout: google.translate.TranslateElement.InlineLayout.SIMPLE,
            autoDisplay: false
        }, 'google_translate_element');
        
        // Restore language from localStorage after init
        setTimeout(() => {
            const savedLang = localStorage.getItem('ev-page-lang');
            if (savedLang && savedLang !== 'en') {
                triggerTranslate(savedLang);
                if(document.getElementById('custom-lang-select')) {
                    document.getElementById('custom-lang-select').value = savedLang;
                }
            }
        }, 1000);
    };

    const gtScript = document.createElement('script');
    gtScript.src = '//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit';
    document.body.appendChild(gtScript);

    // 3. Helper to trigger translation
    function triggerTranslate(langCode) {
        const selectField = document.querySelector("#google_translate_element select");
        if (selectField) {
            selectField.value = langCode;
            selectField.dispatchEvent(new Event('change'));
        }
    }

    // 4. Build Custom UI Dropdown
    const langSelect = document.createElement('select');
    langSelect.id = 'custom-lang-select';
    langSelect.style.cssText = `
        position:fixed;top:70px;right:16px;z-index:9997;
        background:linear-gradient(135deg,#0072ff,#7b2ff7);
        color:#fff;border:none;border-radius:20px;
        padding:8px 16px;font-size:13px;font-weight:700;
        cursor:pointer;box-shadow:0 2px 10px rgba(0,114,255,0.4);
        font-family:'Poppins',sans-serif;letter-spacing:1px;
        appearance:none;-webkit-appearance:none;
        outline:none; text-align:center;
    `;
    
    // Add arrow to select
    const arrowStyle = document.createElement('style');
    arrowStyle.innerHTML = `
    #custom-lang-select {
        background-image: url('data:image/svg+xml;utf8,<svg fill="white" height="24" viewBox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg"><path d="M7 10l5 5 5-5z"/></svg>');
        background-repeat: no-repeat;
        background-position-x: 90%;
        background-position-y: 50%;
        padding-right: 30px !important;
    }
    #custom-lang-select option {
        background: #1e2d40;
        color: #fff;
    }
    `;
    document.head.appendChild(arrowStyle);

    const languages = [
        { code: 'en', name: '🌐 English' },
        { code: 'ta', name: 'தமிழ்' },
        { code: 'hi', name: 'हिंदी' },
        { code: 'ml', name: 'മലയാളം' },
        { code: 'te', name: 'తెలుగు' },
        { code: 'kn', name: 'ಕನ್ನಡ' }
    ];

    const savedLang = localStorage.getItem('ev-page-lang') || 'en';

    languages.forEach(l => {
        const opt = document.createElement('option');
        opt.value = l.code;
        opt.textContent = l.name;
        if (l.code === savedLang) opt.selected = true;
        langSelect.appendChild(opt);
    });

    // 5. Handle change event
    langSelect.addEventListener('change', function(e) {
        const selectedLang = e.target.value;
        localStorage.setItem('ev-page-lang', selectedLang);
        triggerTranslate(selectedLang);
    });

    document.body.appendChild(langSelect);

    // Hide the Google Translate banner at the top
    const hideBannerStyle = document.createElement('style');
    hideBannerStyle.innerHTML = `
        body { top: 0 !important; }
        .skiptranslate iframe { display: none !important; }
        #goog-gt-tt { display: none !important; }
        .goog-te-banner-frame { display: none !important; }
    `;
    document.head.appendChild(hideBannerStyle);

})();
