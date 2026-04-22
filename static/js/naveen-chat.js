// Naveen AI Chatbot - EV Charge Hub
(function() {

const responses = [
  { keys: ['hi','hello','hey','vanakkam','hai'], reply: "Hi there! 👋 I'm <strong>Naveen</strong>, your EV Charge Hub assistant. How can I help you today?" },
  { keys: ['how are you','how r u'], reply: "I'm fully charged and ready to help! ⚡ What can I do for you?" },
  { keys: ['book','slot','booking'], reply: "To book a slot:<br>1. Login → Station → Select Station<br>2. Choose an available slot<br>3. Enter vehicle no & time<br>4. Confirm booking ✅<br>You'll get a QR code instantly!" },
  { keys: ['payment','pay','upi','razorpay','card'], reply: "We support multiple payment options:<br>📱 <strong>UPI</strong> (GPay, PhonePe, Paytm)<br>💳 <strong>Cards</strong> (Debit/Credit)<br>🏦 <strong>NetBanking</strong><br>💵 <strong>Cash</strong> at station" },
  { keys: ['qr','qr code','ticket'], reply: "After booking, you'll get a <strong>QR code ticket</strong> (like BookMyShow!) 🎫<br>Show it at the charging station. It's also sent to your email!" },
  { keys: ['tariff','price','cost','rate','charge','how much'], reply: "Our 2025 charging rates:<br>🔌 Level 1 AC: <strong>₹100</strong>/30 mins<br>⚡ Level 2 AC: <strong>₹200</strong>/30 mins<br>🚀 DC Fast: <strong>₹300</strong>/30 mins<br>🅿️ Parking: <strong>Free!</strong>" },
  { keys: ['station','location','where','nearby','find'], reply: "We have 6 EV stations across Tamil Nadu:<br>📍 Perambalur (2 stations)<br>📍 Chennai<br>📍 Coimbatore<br>📍 Madurai<br>📍 Trichy<br>Use the <strong>Station</strong> page to find nearest one!" },
  { keys: ['cancel','cancellation'], reply: "To cancel a booking:<br>Go to Station → Your Slot → Click <strong>OUT</strong><br>⚠️ Cancellation only allowed before charging starts." },
  { keys: ['reschedule','change time','rebook'], reply: "You can reschedule your booking!<br>Go to Station → Your Slot → Click <strong>Reschedule</strong> 📅" },
  { keys: ['wait','waiting','time pass','bored'], reply: "While charging, visit our <strong>Wait Room</strong>! 🎮<br>🐍 Play Snake game<br>💡 Learn EV facts<br>📰 Read TN EV news<br>Click 'Wait Room' button on your slot!" },
  { keys: ['register','signup','new user','create account'], reply: "To register:<br>Click <strong>User → Register</strong> on homepage<br>Fill name, address, mobile, email, username & password<br>You'll get a welcome email! 📧" },
  { keys: ['forgot','password','reset'], reply: "Forgot password? No worries!<br>Go to Login page → Click <strong>'Forgot Password?'</strong><br>Enter your email → Get reset link 📧" },
  { keys: ['contact','support','help','problem','issue','customer','care'], reply: "Need help? Contact us:<br>📧 Email: evcharge@info.com<br>📱 Customer Care: <strong><a href='tel:6379241960' style='color:#00c6ff;'>+91 63792 41960</a></strong><br>Or describe your issue here and I'll try to help! 😊" },
  { keys: ['active','online','status'], reply: "Station status is shown in real-time on the Station page! 🟢 Green = Active, 🔴 Red = Inactive" },
  { keys: ['ev','electric','vehicle','car'], reply: "EV Charge Hub supports all electric vehicles — 2-wheelers, 4-wheelers, and commercial EVs! ⚡🚗" },
  { keys: ['thank','thanks','thank you','thx'], reply: "You're welcome! 😊 Happy charging! ⚡ Is there anything else I can help you with?" },
  { keys: ['bye','goodbye','ok bye','cya'], reply: "Goodbye! 👋 Drive safe and stay charged! ⚡ Come back anytime!" },
  { keys: ['naveen','who are you','your name'], reply: "I'm <strong>Naveen</strong> 🤖, the AI assistant for EV Charge Hub! I'm here to help you with bookings, payments, stations, and more. Ask me anything!" },
];

const defaultReply = "I'm not sure about that 🤔 But I can help you with:<br>• Slot booking<br>• Payment options<br>• Station locations<br>• Tariff rates<br>• Account issues<br><br>Type your question or call us at <strong><a href='tel:6379241960' style='color:#00c6ff;'>+91 63792 41960</a></strong> 📞";

function getReply(msg) {
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
    <div class="name">Naveen</div>
    <div class="status">🟢 Online · EV Assistant</div>
  </div>
  <button id="naveen-close">✕</button>
</div>
<div id="naveen-msgs"></div>
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

btn.onclick = () => {
  opened = !opened;
  box.style.display = opened ? 'flex' : 'none';
  btn.innerHTML = opened ? '✕' : '💬';
  if (opened && msgs.children.length === 0) {
    setTimeout(() => addMsg("Hi! 👋 I'm <strong>Naveen</strong>, your EV Charge Hub assistant.<br>How can I help you today?", 'bot'), 400);
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
