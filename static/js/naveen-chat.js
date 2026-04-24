// Naveen AI Chatbot - EV Charge Hub
(function() {

let lang = localStorage.getItem('ev-chat-lang') || 'en';

const responses = {
  en: [
    { keys: ['hi','hello','hey','vanakkam','hai','good morning','good evening'], reply: "Hi there! 👋 I'm <strong>Naveen</strong>, your EV Charge Hub assistant. How can I help you today?" },
    { keys: ['how are you','how r u'], reply: "I'm fully charged and ready to help! ⚡ What can I do for you?" },
    { keys: ['book','slot','booking','how to book'], reply: "To book a slot:<br>1. Login → Station → Select Station<br>2. Choose an available slot<br>3. Enter vehicle no & time<br>4. Confirm booking ✅<br>You'll get a QR code instantly!" },
    { keys: ['payment','pay','upi','razorpay','card','how to pay'], reply: "We support multiple payment options:<br>📱 <strong>UPI</strong> (GPay, PhonePe, Paytm)<br>💳 <strong>Cards</strong> (Debit/Credit)<br>🏦 <strong>NetBanking</strong><br>💵 <strong>Cash</strong> at station" },
    { keys: ['qr','qr code','ticket'], reply: "After booking, you'll get a <strong>QR code ticket</strong> 🎫<br>Show it at the charging station. It's also sent to your email!" },
    { keys: ['tariff','price','cost','rate','how much','charges'], reply: "Our charging rates:<br>🔌 AC Level 1: <strong>₹100</strong>/30 mins<br>⚡ AC Level 2: <strong>₹200</strong>/30 mins<br>🚀 DC Fast: <strong>₹300</strong>/30 mins<br>🅿️ Parking: <strong>Free!</strong>" },
    { keys: ['station','location','where','nearby','find','which station'], reply: "We have EV stations across Tamil Nadu:<br>📍 Perambalur (2 stations)<br>📍 Chennai<br>📍 Coimbatore<br>📍 Madurai<br>📍 Trichy<br>Use the <strong>Station</strong> page to find nearest one!" },
    { keys: ['cancel','cancellation','cancel booking'], reply: "To cancel a booking:<br>Go to Station → Your Slot → Click <strong>OUT</strong><br>⚠️ Cancellation only allowed before charging starts." },
    { keys: ['reschedule','change time','rebook','change booking'], reply: "You can reschedule your booking!<br>Go to Station → Your Slot → Click <strong>Reschedule</strong> 📅" },
    { keys: ['wait','waiting','game','bored','time pass'], reply: "While charging, visit our <strong>Wait Room</strong>! 🎮<br>🏎️ Play EV Car Racing game<br>💡 Learn EV facts<br>📰 Read TN EV news<br>Click 'Wait Room' button on your slot!" },
    { keys: ['register','signup','new user','create account','how to register'], reply: "To register:<br>Click <strong>User → Register</strong> on homepage<br>Fill name, address, mobile, email, username & password<br>You'll get a welcome email! 📧" },
    { keys: ['forgot','password','reset','forgot password'], reply: "Forgot password?<br>Go to Login page → Click <strong>'Forgot Password?'</strong><br>Enter your email → Get OTP → Reset password 📧" },
    { keys: ['contact','support','help','problem','issue','customer','care','complaint'], reply: "Need help? Contact us:<br>📧 Email: evcharge@info.com<br>📱 Customer Care: <strong><a href='tel:6379241960' style='color:#00c6ff;'>+91 63792 41960</a></strong><br>Or describe your issue here! 😊" },
    { keys: ['active','online','status','station status'], reply: "Station status is shown in real-time! 🟢 Green = Active, 🔴 Red = Inactive<br>Check the Station page for live status." },
    { keys: ['ev','electric','vehicle','car','bike','two wheeler'], reply: "EV Charge Hub supports all electric vehicles — 2-wheelers, 4-wheelers, and commercial EVs! ⚡🚗" },
    { keys: ['ac','ac charging','ac level'], reply: "AC Charging options:<br>🔌 <strong>AC Level 1</strong> - ₹100/30 mins (Slow)<br>⚡ <strong>AC Level 2</strong> - ₹200/30 mins (Fast)" },
    { keys: ['dc','dc fast','dc charging','fast charge'], reply: "🚀 <strong>DC Fast Charging</strong> - ₹300/30 mins<br>Ultra-fast charging! Up to 90 miles range in just 30 minutes!" },
    { keys: ['slot full','no slot','slot available','available'], reply: "If slots are full, try:<br>1. Different time slot<br>2. Different station<br>3. Come back later - slots free up after charging completes!" },
    { keys: ['otp','verification','verify'], reply: "OTP is sent to your registered email/mobile.<br>Check spam folder if not received.<br>Click <strong>Resend OTP</strong> if expired!" },
    { keys: ['thank','thanks','thank you','thx','ok'], reply: "You're welcome! 😊 Happy charging! ⚡ Is there anything else I can help you with?" },
    { keys: ['bye','goodbye','ok bye','cya'], reply: "Goodbye! 👋 Drive safe and stay charged! ⚡" },
    { keys: ['naveen','who are you','your name'], reply: "I'm <strong>Naveen</strong> 🤖, the AI assistant for EV Charge Hub! Ask me anything about bookings, payments, stations, and more!" },
  ],
  ta: [
    { keys: ['hi','hello','hey','vanakkam','hai','காலை வணக்கம்','மாலை வணக்கம்'], reply: "வணக்கம்! 👋 நான் <strong>நவீன்</strong>, உங்கள் EV Charge Hub உதவியாளர். எப்படி உதவலாம்?" },
    { keys: ['how are you','how r u','நலமா'], reply: "நான் சார்ஜ் ஆகி தயாராக இருக்கேன்! ⚡ என்ன உதவி வேணும்?" },
    { keys: ['book','slot','booking','புக்','ஸ்லாட்'], reply: "ஸ்லாட் புக் பண்ண:<br>1. Login → Station → Station Select பண்ணுங்க<br>2. Available slot தேர்வு பண்ணுங்க<br>3. Vehicle no & time enter பண்ணுங்க<br>4. Booking confirm ✅<br>உடனே QR code கிடைக்கும்!" },
    { keys: ['payment','pay','upi','பணம்','கட்டணம்'], reply: "பல payment options இருக்கு:<br>📱 <strong>UPI</strong> (GPay, PhonePe, Paytm)<br>💳 <strong>Cards</strong> (Debit/Credit)<br>🏦 <strong>NetBanking</strong><br>💵 <strong>Cash</strong> station-ல" },
    { keys: ['tariff','price','cost','rate','எவ்வளவு','கட்டணம்'], reply: "சார்ஜிங் கட்டணம்:<br>🔌 AC Level 1: <strong>₹100</strong>/30 நிமிடம்<br>⚡ AC Level 2: <strong>₹200</strong>/30 நிமிடம்<br>🚀 DC Fast: <strong>₹300</strong>/30 நிமிடம்" },
    { keys: ['station','location','where','nearby','எங்கே','station எங்க'], reply: "Tamil Nadu-ல EV stations இருக்கு:<br>📍 பெரம்பலூர் (2 stations)<br>📍 சென்னை<br>📍 கோயம்புத்தூர்<br>📍 மதுரை<br>📍 திருச்சி" },
    { keys: ['cancel','cancellation','cancel','ரத்து'], reply: "Booking ரத்து பண்ண:<br>Station → Your Slot → <strong>OUT</strong> click பண்ணுங்க<br>⚠️ Charging start ஆகுமுன்னாடி மட்டும் cancel பண்ணலாம்." },
    { keys: ['contact','support','help','problem','உதவி','complaint','புகார்'], reply: "உதவிக்கு தொடர்பு கொள்ளுங்க:<br>📧 Email: evcharge@info.com<br>📱 Customer Care: <strong><a href='tel:6379241960' style='color:#00c6ff;'>+91 63792 41960</a></strong>" },
    { keys: ['forgot','password','reset','password மறந்து'], reply: "Password மறந்துட்டீங்களா?<br>Login page → <strong>'Forgot Password?'</strong> click பண்ணுங்க<br>Email enter → OTP வரும் → Password reset பண்ணலாம் 📧" },
    { keys: ['register','signup','new user','register பண்ண'], reply: "Register பண்ண:<br><strong>User → Register</strong> click பண்ணுங்க<br>Name, address, mobile, email, username & password fill பண்ணுங்க<br>Welcome email வரும்! 📧" },
    { keys: ['thank','thanks','நன்றி','சரி'], reply: "நன்றி! 😊 Happy charging! ⚡ வேற ஏதாவது உதவி வேணுமா?" },
    { keys: ['bye','goodbye','சரி bye','போகிறேன்'], reply: "சரி! 👋 Safe-ஆ போங்க! ⚡" },
  ]
};

const defaultReply = {
  en: "I'm not sure about that 🤔 But I can help you with:<br>• Slot booking<br>• Payment options<br>• Station locations<br>• Tariff rates<br>• Account issues<br><br>Call us: <strong><a href='tel:6379241960' style='color:#00c6ff;'>+91 63792 41960</a></strong> 📞",
  ta: "அது பத்தி தெரியல 🤔 ஆனா இதுல உதவலாம்:<br>• Slot booking<br>• Payment options<br>• Station locations<br>• கட்டணம்<br><br>Call பண்ணுங்க: <strong><a href='tel:6379241960' style='color:#00c6ff;'>+91 63792 41960</a></strong> 📞"
};

function getReply(msg) {
  const lower = msg.toLowerCase();
  const list = responses[lang] || responses['en'];
  for (const r of list) {
    if (r.keys.some(k => lower.includes(k))) return r.reply;
  }
  return defaultReply[lang];
}

  }
  return defaultReply[lang] || defaultReply['en'];
}

// Build UI
const style = document.createElement('style');
style.textContent = `
#naveen-btn{position:fixed;bottom:24px;right:24px;width:56px;height:56px;border-radius:50%;background:linear-gradient(135deg,#0072ff,#7b2ff7);border:none;cursor:pointer;box-shadow:0 4px 20px rgba(0,114,255,0.5);z-index:9999;font-size:24px;color:#fff;transition:transform 0.2s;}
#naveen-btn:hover{transform:scale(1.1);}
#naveen-box{position:fixed;bottom:90px;right:24px;width:320px;background:#0d1117;border-radius:16px;box-shadow:0 8px 40px rgba(0,0,0,0.5);z-index:9999;display:none;flex-direction:column;overflow:hidden;border:1px solid #1e2d40;font-family:'Poppins',sans-serif;}
#naveen-header{background:linear-gradient(90deg,#0072ff,#7b2ff7);padding:14px 16px;display:flex;align-items:center;gap:10px;}
#naveen-header .avatar{width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,0.2);display:flex;align-items:center;justify-content:center;font-size:18px;}
#naveen-header .info .name{color:#fff;font-weight:700;font-size:14px;}
#naveen-header .info .status{color:rgba(255,255,255,0.7);font-size:11px;}
#naveen-close{margin-left:auto;background:none;border:none;color:#fff;font-size:18px;cursor:pointer;padding:0 4px;}
#naveen-lang{background:rgba(255,255,255,0.2);border:none;color:#fff;font-size:11px;cursor:pointer;padding:3px 8px;border-radius:10px;margin-right:4px;font-weight:700;}
#naveen-msgs{height:280px;overflow-y:auto;padding:12px;display:flex;flex-direction:column;gap:8px;}
#naveen-msgs::-webkit-scrollbar{width:4px;}
#naveen-msgs::-webkit-scrollbar-thumb{background:#1e2d40;border-radius:4px;}
.msg-bot,.msg-user{max-width:85%;padding:8px 12px;border-radius:12px;font-size:13px;line-height:1.5;}
.msg-bot{background:#131920;color:#e2e8f0;border-bottom-left-radius:4px;align-self:flex-start;}
.msg-user{background:linear-gradient(90deg,#0072ff,#7b2ff7);color:#fff;border-bottom-right-radius:4px;align-self:flex-end;}
#naveen-input-row{display:flex;padding:10px;gap:8px;border-top:1px solid #1e2d40;}
#naveen-input{flex:1;background:#131920;border:1px solid #1e2d40;border-radius:20px;padding:8px 14px;color:#fff;font-size:13px;outline:none;font-family:'Poppins',sans-serif;}
#naveen-input::placeholder{color:#4a5568;}
#naveen-send{background:linear-gradient(90deg,#0072ff,#7b2ff7);border:none;border-radius:50%;width:36px;height:36px;color:#fff;cursor:pointer;font-size:16px;}
.typing{display:flex;gap:4px;align-items:center;padding:8px 12px;}
.typing span{width:6px;height:6px;background:#4a9eff;border-radius:50%;animation:bounce 1s infinite;}
.typing span:nth-child(2){animation-delay:0.2s;}
.typing span:nth-child(3){animation-delay:0.4s;}
@keyframes bounce{0%,100%{transform:translateY(0);}50%{transform:translateY(-4px);}}
.quick-btns{display:flex;flex-wrap:wrap;gap:6px;padding:8px 12px;border-top:1px solid #1e2d40;}
.quick-btn{background:#131920;border:1px solid #1e2d40;color:#4a9eff;font-size:11px;padding:4px 10px;border-radius:12px;cursor:pointer;transition:all 0.2s;}
.quick-btn:hover{background:#0072ff;color:#fff;border-color:#0072ff;}
`;
document.head.appendChild(style);

const btn = document.createElement('button');
btn.id = 'naveen-btn';
btn.innerHTML = '💬';
btn.title = 'Chat with Naveen';

const box = document.createElement('div');
box.id = 'naveen-box';
box.innerHTML = `
<div id="naveen-header">
  <div class="avatar">🤖</div>
  <div class="info">
    <div class="name">Naveen AI</div>
    <div class="status">🟢 Online · EV Assistant</div>
  </div>
  <button id="naveen-lang" title="Switch Language">EN</button>
  <button id="naveen-close">✕</button>
</div>
<div id="naveen-msgs"></div>
<div class="quick-btns">
  <button class="quick-btn" onclick="quickAsk('How to book?')">📅 Book</button>
  <button class="quick-btn" onclick="quickAsk('Payment options')">💳 Pay</button>
  <button class="quick-btn" onclick="quickAsk('Tariff rates')">💰 Rates</button>
  <button class="quick-btn" onclick="quickAsk('Contact support')">📞 Help</button>
</div>
<div id="naveen-input-row">
  <input id="naveen-input" placeholder="Ask me anything..." autocomplete="off">
  <button id="naveen-send">➤</button>
</div>`;

document.body.appendChild(btn);
document.body.appendChild(box);

const msgs = document.getElementById('naveen-msgs');
const input = document.getElementById('naveen-input');
let opened = false;

function addMsg(text, type) {
  const d = document.createElement('div');
  d.className = type === 'bot' ? 'msg-bot' : 'msg-user';
  d.innerHTML = text;
  msgs.appendChild(d);
  msgs.scrollTop = msgs.scrollHeight;
}

function showTyping() {
  const d = document.createElement('div');
  d.className = 'msg-bot typing';
  d.id = 'typing-indicator';
  d.innerHTML = '<span></span><span></span><span></span>';
  msgs.appendChild(d);
  msgs.scrollTop = msgs.scrollHeight;
}

function removeTyping() {
  const t = document.getElementById('typing-indicator');
  if (t) t.remove();
}

function sendMsg() {
  const text = input.value.trim();
  if (!text) return;
  addMsg(text, 'user');
  input.value = '';
  showTyping();
  setTimeout(() => {
    removeTyping();
    addMsg(getReply(text), 'bot');
  }, 800);
}

function quickAsk(text) {
  addMsg(text, 'user');
  showTyping();
  setTimeout(() => {
    removeTyping();
    addMsg(getReply(text), 'bot');
  }, 600);
}

btn.onclick = () => {
  opened = !opened;
  box.style.display = opened ? 'flex' : 'none';
  btn.innerHTML = opened ? '✕' : '💬';
  if (opened && msgs.children.length === 0) {
    const greeting = lang === 'ta' 
      ? "வணக்கம்! 👋 நான் <strong>நவீன்</strong>. EV Charge Hub-ல உங்களுக்கு உதவ இங்கே இருக்கேன்!<br><br>என்னை கேளுங்க - booking, payment, station எதுவும் சொல்லுங்க! 😊"
      : "Hi! 👋 I'm <strong>Naveen</strong>. I'm here to help you with EV Charge Hub!<br><br>Ask me anything about booking, payment, stations, or any issue! 😊";
    setTimeout(() => addMsg(greeting, 'bot'), 400);
  }
};

// Language toggle
document.getElementById('naveen-lang').onclick = () => {
  lang = lang === 'en' ? 'ta' : 'en';
  localStorage.setItem('ev-chat-lang', lang);
  document.getElementById('naveen-lang').textContent = lang === 'en' ? 'EN' : 'தமிழ்';
  const switchMsg = lang === 'ta' ? "தமிழ் மொழிக்கு மாறினோம்! 🙏" : "Switched to English! 🙏";
  addMsg(switchMsg, 'bot');
};

// Set initial lang button text
document.getElementById('naveen-lang').textContent = lang === 'en' ? 'EN' : 'தமிழ்';

document.getElementById('naveen-close').onclick = () => {
  opened = false;
  box.style.display = 'none';
  btn.innerHTML = '💬';
};

document.getElementById('naveen-send').onclick = sendMsg;
input.addEventListener('keydown', e => { if (e.key === 'Enter') sendMsg(); });

})();
