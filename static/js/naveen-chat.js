// Naveen AI Chatbot - EV Charge Hub - Realtime Multi-lingual
(function() {

const responses = [
  { keys: ['hi','hello','hey','vanakkam','hai','good morning','good evening'], reply: "Hey buddy! 👋 I'm <strong>Naveen</strong>, your EV Charge Hub buddy! What's up? How can I help you out today?" },
  { keys: ['how are you','how r u'], reply: "I'm fully charged and feeling awesome! ⚡ What about you? Need any help?" },
  { keys: ['book','slot','booking','how to book'], reply: "Booking a slot is super easy! 😎<br>1. Just Login and go to Station<br>2. Pick a station and an open slot<br>3. Punch in your vehicle no. & time<br>4. Confirm it! ✅<br>Boom! You'll get your QR code right away." },
  { keys: ['payment','pay','upi','razorpay','card','how to pay'], reply: "No worries about payment, we got all options covered for you!<br>📱 <strong>UPI</strong> (GPay, PhonePe, Paytm)<br>💳 <strong>Cards</strong> (Debit/Credit)<br>🏦 <strong>NetBanking</strong><br>💵 Or just pay <strong>Cash</strong> at the station!" },
  { keys: ['qr','qr code','ticket'], reply: "Once you book, you'll get a cool <strong>QR code ticket</strong> 🎫<br>Just flash it at the station when you arrive. I'll also drop it in your email so you don't lose it!" },
  { keys: ['tariff','price','cost','rate','how much','charges'], reply: "Here are our super affordable rates:<br>🔌 AC Level 1: <strong>₹100</strong> for 30 mins<br>⚡ AC Level 2: <strong>₹200</strong> for 30 mins<br>🚀 DC Fast: <strong>₹300</strong> for 30 mins<br>🅿️ And hey, Parking is totally <strong>Free!</strong> 😉" },
  { keys: ['station','location','where','nearby','find','which station'], reply: "We are all over Tamil Nadu, bro! 🗺️<br>📍 Perambalur (2 spots!)<br>📍 Chennai<br>📍 Coimbatore<br>📍 Madurai<br>📍 Trichy<br>Check out the <strong>Station</strong> page to find the one closest to you!" },
  { keys: ['cancel','cancellation','cancel booking'], reply: "Change of plans? No problem! 🔄<br>Go to Station → Your Slot → Just hit <strong>OUT</strong> to cancel.<br>⚠️ Just make sure you do it before your charging session starts!" },
  { keys: ['reschedule','change time','rebook','change booking'], reply: "Running late? You can totally reschedule! 📅<br>Head to Station → Your Slot → and click <strong>Reschedule</strong> to pick a new time." },
  { keys: ['wait','waiting','game','bored','time pass'], reply: "Getting bored while charging? Hop into our <strong>Wait Room</strong>! 🎮<br>🏎️ Play some EV Car Racing!<br>💡 Read cool EV facts<br>📰 Catch up on TN EV news<br>Just hit the 'Wait Room' button on your slot!" },
  { keys: ['register','signup','new user','create account','how to register'], reply: "Awesome, you want to join us? 🎉<br>Just click <strong>User → Register</strong> on the homepage.<br>Fill in your details, set up a cool username, and you're in! You'll get a welcome email from us too! 📧" },
  { keys: ['forgot','password','reset','forgot password'], reply: "Forgot your password? Happens to the best of us! 😅<br>Head to the Login page → Click <strong>'Forgot Password?'</strong><br>Pop in your email, grab the OTP, and reset it. Easy peasy!" },
  { keys: ['contact','support','help','problem','issue','customer','care','complaint'], reply: "Got a problem? Don't stress, we're here for you! 🤝<br>📧 Drop an email at: evcharge@info.com<br>📱 Call our Customer Care buddy: <strong><a href='tel:6379241960' style='color:#00c6ff;'>+91 63792 41960</a></strong><br>Or just tell me right here! 😊" },
  { keys: ['active','online','status','station status'], reply: "You can see if a station is active right on the map! 🟢 Green means it's ready, 🔴 Red means it's offline.<br>Check the Station page for live updates!" },
  { keys: ['ev','electric','vehicle','car','bike','two wheeler'], reply: "We love all EVs! ⚡🚗 Whether you've got a cool electric bike, a car, or even a commercial EV, our hubs support them all!" },
  { keys: ['ac','ac charging','ac level'], reply: "For AC Charging, we have:<br>🔌 <strong>AC Level 1</strong> - ₹100/30 mins (Relaxed charging)<br>⚡ <strong>AC Level 2</strong> - ₹200/30 mins (A bit faster!)" },
  { keys: ['dc','dc fast','dc charging','fast charge'], reply: "In a hurry? Use our 🚀 <strong>DC Fast Charging</strong> for ₹300/30 mins!<br>It's ultra-fast, getting you up to 90 miles of range in just half an hour! Zoom zoom! 🏎️" },
  { keys: ['slot full','no slot','slot available','available'], reply: "Ah man, slots are full? 😕 Don't worry, you can try:<br>1. Picking a different time<br>2. Checking a nearby station<br>3. Or just chill for a bit, slots open up all the time as cars finish charging!" },
  { keys: ['otp','verification','verify'], reply: "We just sent an OTP to your email/mobile! 📩<br>If you don't see it, take a quick peek in your spam folder.<br>If it expired, just hit <strong>Resend OTP</strong>!" },
  { keys: ['thank','thanks','thank you','thx','ok'], reply: "Anytime, buddy! 😊 Happy to help! Anything else you need?" },
  { keys: ['bye','goodbye','ok bye','cya'], reply: "Catch you later, bro! 👋 Drive safe and keep that battery topped up! ⚡" },
  { keys: ['naveen','who are you','your name'], reply: "I'm <strong>Naveen</strong> 🤖, your friendly neighborhood AI assistant for EV Charge Hub! Ask me anything, I'm here to chat!" },
];

const defaultReply = "Oops, I'm not totally sure about that one! 🤔 But hey, I can definitely help you out with:<br>• Booking a slot<br>• How to pay<br>• Finding a station<br>• Checking out the prices<br>• Fixing account issues<br><br>Or you can always give our awesome team a call: <strong><a href='tel:6379241960' style='color:#00c6ff;'>+91 63792 41960</a></strong> 📞";

// Language detection state
let userLang = 'en';

async function translateText(text, targetLang, sourceLang='auto') {
  if (targetLang === 'en' && sourceLang === 'en') return { text, detectedLang: 'en' };
  try {
    const url = `https://translate.googleapis.com/translate_a/single?client=gtx&sl=${sourceLang}&tl=${targetLang}&dt=t&q=${encodeURIComponent(text)}`;
    const response = await fetch(url);
    const data = await response.json();
    let translated = '';
    data[0].forEach(part => { translated += part[0]; });
    const detectedLang = data[2] || targetLang; // Data[2] contains detected source lang
    return { text: translated, detectedLang };
  } catch (e) {
    console.error("Translation error:", e);
    return { text, detectedLang: 'en' };
  }
}

function getReplyEnglish(msg) {
  const lower = msg.toLowerCase();
  for (const r of responses) {
    if (r.keys.some(k => lower.includes(k))) return r.reply;
  }
  return defaultReply;
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
    <div class="status">🟢 Auto-Translate Active</div>
  </div>
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
  <input id="naveen-input" placeholder="Ask in any language..." autocomplete="off">
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

async function handleChat(text) {
  addMsg(text, 'user');
  input.value = '';
  showTyping();

  try {
    // 1. Translate user input to English to understand intent
    const translatedToEn = await translateText(text, 'en', 'auto');
    userLang = translatedToEn.detectedLang; // update user language
    
    // 2. Get the English reply
    const englishReply = getReplyEnglish(translatedToEn.text);
    
    // 3. Translate the reply back to the user's language
    let finalReply = englishReply;
    if (userLang && userLang !== 'en') {
        const translatedToUserLang = await translateText(englishReply, userLang, 'en');
        finalReply = translatedToUserLang.text;
    }
    
    removeTyping();
    addMsg(finalReply, 'bot');
  } catch (e) {
    removeTyping();
    addMsg("Sorry, I'm having trouble understanding right now.", 'bot');
  }
}

async function sendMsg() {
  const text = input.value.trim();
  if (!text) return;
  await handleChat(text);
}

window.quickAsk = async function(text) {
    await handleChat(text);
};

btn.onclick = () => {
  opened = !opened;
  box.style.display = opened ? 'flex' : 'none';
  btn.innerHTML = opened ? '✕' : '💬';
  if (opened && msgs.children.length === 0) {
    const greeting = "Hey buddy! 👋 I'm <strong>Naveen</strong>! I can chat with you in any language you want! <br><br>Ask me anything about booking, payment, or whatever's on your mind! 😊";
    setTimeout(() => addMsg(greeting, 'bot'), 400);
  }
};

document.getElementById('naveen-close').onclick = () => {
  opened = false;
  box.style.display = 'none';
  btn.innerHTML = '💬';
};

document.getElementById('naveen-send').onclick = sendMsg;
input.addEventListener('keydown', e => { if (e.key === 'Enter') sendMsg(); });

})();
