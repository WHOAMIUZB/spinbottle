// =============================================================================
// Spin the Bottle — Mini App frontend
// =============================================================================
const tg = window.Telegram ? window.Telegram.WebApp : null;
if (tg) { tg.ready(); tg.expand(); }

// DEV rejimda (Telegramsiz brauzerda test qilish uchun) tasodifiy foydalanuvchi ID
const DEV_USER_ID = (() => {
  let id = localStorage.getItem('dev_user_id');
  if (!id) {
    id = String(900000000 + Math.floor(Math.random() * 99999));
    localStorage.setItem('dev_user_id', id);
  }
  return id;
})();

const initData = tg && tg.initData ? tg.initData : null;

async function api(path, { method = 'GET', body = null } = {}) {
  const headers = { 'Content-Type': 'application/json' };
  let url = path;
  if (initData) {
    headers['X-Init-Data'] = initData;
  } else {
    url += (path.includes('?') ? '&' : '?') + 'dev_user_id=' + DEV_USER_ID;
  }
  const res = await fetch(url, { method, headers, body: body ? JSON.stringify(body) : null });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Xatolik' }));
    throw new Error(err.detail || 'Xatolik yuz berdi');
  }
  return res.json();
}

function toast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  clearTimeout(toast._timer);
  toast._timer = setTimeout(() => t.classList.remove('show'), 2200);
}

// ------------------------------------------------------------------
// STATE
// ------------------------------------------------------------------
const state = {
  me: null,
  room: null,
  reactions: [],
  wheelPrizes: [],
  shopPackages: [],
  settings: {},
  selectedTarget: null,
  ws: null,
};

// ------------------------------------------------------------------
// INIT
// ------------------------------------------------------------------
async function init() {
  try {
    const [me, settings, reactions, wheelPrizes, shopPackages] = await Promise.all([
      api('/api/me'), api('/api/settings'), api('/api/reactions'),
      api('/api/wheel-prizes'), api('/api/shop-packages'),
    ]);
    state.me = me; state.settings = settings; state.reactions = reactions;
    state.wheelPrizes = wheelPrizes; state.shopPackages = shopPackages;

    renderMe();
    renderShop();
    renderFreeLabels();
    renderWheel();
    await loadRoom();
    await loadChat();
    connectWs();

    if (me.is_admin) {
      document.getElementById('railAdmin').style.display = 'flex';
    }
  } catch (e) {
    console.error(e);
    toast('Ulanishda xatolik: ' + e.message);
  }
}

function renderMe() {
  document.getElementById('heartsCount').textContent = state.me.hearts;
  document.getElementById('meName').textContent = state.me.first_name || state.me.username || 'Siz';
  document.getElementById('meAvatar').textContent = (state.me.first_name || '?').slice(0, 2).toUpperCase();
  document.getElementById('settingsIdLabel').textContent = 'ID: ' + state.me.id;
}

async function loadRoom() {
  const data = await api('/api/room');
  state.room = data;
  document.getElementById('roomLabel').textContent = 'Стол ' + (data.room ? data.room.id.toString().padStart(3, '0') : '—');
  renderSeats(data.users);
}

const SEAT_POSITIONS = [
  [50, 6], [85, 20], [96, 50], [85, 80], [50, 94], [15, 80], [4, 50], [15, 20],
];

function renderSeats(users) {
  const ring = document.getElementById('seatsRing');
  ring.innerHTML = '';
  users.forEach((u, i) => {
    const pos = SEAT_POSITIONS[i % SEAT_POSITIONS.length];
    const el = document.createElement('div');
    el.className = 'seat' + (u.id === state.me.id ? ' me' : '');
    el.style.setProperty('--sx', pos[0] + '%');
    el.style.setProperty('--sy', pos[1] + '%');
    el.dataset.userId = u.id;
    el.innerHTML = `
      <img class="seat-avatar" src="${u.photo_url || fallbackAvatar(u)}" alt="">
      ${u.is_vip ? '<div class="seat-badge">👑</div>' : ''}
      <div class="seat-name">${escapeHtml(u.first_name || 'Do\'st')}</div>
    `;
    el.addEventListener('click', () => openGiftModal(u.id));
    ring.appendChild(el);
  });
}

function fallbackAvatar(u) {
  const initials = (u.first_name || '?').slice(0, 1).toUpperCase();
  return 'data:image/svg+xml;utf8,' + encodeURIComponent(
    `<svg xmlns="http://www.w3.org/2000/svg" width="56" height="56"><rect width="100%" height="100%" fill="#5c3413"/><text x="50%" y="58%" font-size="24" fill="#fff" text-anchor="middle" font-family="sans-serif">${initials}</text></svg>`
  );
}

function escapeHtml(s) {
  return (s || '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

// ------------------------------------------------------------------
// CHAT
// ------------------------------------------------------------------
async function loadChat() {
  const msgs = await api('/api/chat');
  const box = document.getElementById('chatMessages');
  box.innerHTML = '';
  msgs.forEach(appendChatMessage);
  box.scrollTop = box.scrollHeight;
}

function appendChatMessage(m) {
  const box = document.getElementById('chatMessages');
  const div = document.createElement('div');
  div.className = 'chat-msg';
  div.innerHTML = `<div class="bubble"><span class="name">${escapeHtml(m.first_name || 'Foydalanuvchi')}:</span>${escapeHtml(m.text || '')}</div>`;
  box.appendChild(div);
  box.scrollTop = box.scrollHeight;
}

document.getElementById('chatForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const input = document.getElementById('chatInput');
  const text = input.value.trim();
  if (!text) return;
  input.value = '';
  try { await api('/api/chat', { method: 'POST', body: { text } }); }
  catch (e) { toast(e.message); }
});

// ------------------------------------------------------------------
// WEBSOCKET (real vaqt yangilanishlar)
// ------------------------------------------------------------------
function connectWs() {
  if (!state.room || !state.room.room) return;
  const proto = location.protocol === 'https:' ? 'wss' : 'ws';
  const ws = new WebSocket(`${proto}://${location.host}/ws/room/${state.room.room.id}`);
  ws.onmessage = (evt) => {
    const msg = JSON.parse(evt.data);
    if (msg.event === 'chat' && msg.data.user_id !== state.me.id) {
      appendChatMessage(msg.data);
    } else if (msg.event === 'spin_bottle') {
      playSpinAnimation(msg.data);
    } else if (msg.event === 'reaction') {
      if (msg.data.to === state.me.id) refreshHearts();
    } else if (msg.event === 'wheel_win') {
      // boshqalar yutganda kichik bildirishnoma (ixtiyoriy)
    }
  };
  ws.onclose = () => setTimeout(connectWs, 3000);
  state.ws = ws;
}

async function refreshHearts() {
  const me = await api('/api/me');
  state.me = me;
  document.getElementById('heartsCount').textContent = me.hearts;
}

// ------------------------------------------------------------------
// BOTTLE SPIN
// ------------------------------------------------------------------
document.getElementById('bottleBtn').addEventListener('click', async () => {
  try {
    const result = await api('/api/spin-bottle', { method: 'POST' });
    playSpinAnimation(result);
  } catch (e) { toast(e.message); }
});

function playSpinAnimation(result) {
  const rotor = document.getElementById('bottleRotor');
  const finalAngle = 360 * 4 + Math.floor(Math.random() * 360);
  rotor.style.setProperty('--final-angle', finalAngle + 'deg');
  rotor.classList.remove('spinning');
  void rotor.offsetWidth; // reflow -> animatsiyani qayta ishga tushirish
  rotor.style.animationDuration = '2.4s';
  rotor.classList.add('spinning');

  const banner = document.getElementById('outcomeBanner');
  setTimeout(() => {
    const names = result.pair.map(p => p.first_name || 'Do\'st').join(' ❤️ ');
    banner.textContent = `${names}: ${result.outcome}`;
    banner.classList.add('show');
    setTimeout(() => banner.classList.remove('show'), 3200);
  }, 2450);
}

// ------------------------------------------------------------------
// MODALS - umumiy ochish/yopish
// ------------------------------------------------------------------
function openModal(id) { document.getElementById(id).classList.add('open'); }
function closeModal(id) { document.getElementById(id).classList.remove('open'); }
document.querySelectorAll('[data-close]').forEach(btn => {
  btn.addEventListener('click', () => closeModal(btn.dataset.close));
});
document.querySelectorAll('.modal-overlay').forEach(ov => {
  ov.addEventListener('click', (e) => { if (e.target === ov) ov.classList.remove('open'); });
});

document.getElementById('railShop').addEventListener('click', () => openModal('shopModal'));
document.getElementById('heartsPill').addEventListener('click', () => openModal('shopModal'));
document.getElementById('railWheel').addEventListener('click', () => openModal('wheelModal'));
document.getElementById('railFree').addEventListener('click', () => openModal('freeModal'));
document.getElementById('railSettings').addEventListener('click', () => openModal('settingsModal'));
document.getElementById('settingsBtn').addEventListener('click', () => openModal('settingsModal'));
document.getElementById('railAdmin').addEventListener('click', () => {
  const url = '/admin' + (initData ? '' : '?dev_user_id=' + DEV_USER_ID);
  if (tg && tg.openLink) tg.openLink(location.origin + url); else window.open(url, '_blank');
});
document.getElementById('giftPickerBtn').addEventListener('click', () => openGiftModal());

// ------------------------------------------------------------------
// DO'KON (Shop)
// ------------------------------------------------------------------
function renderShop() {
  const grid = document.getElementById('shopGrid');
  grid.innerHTML = '';
  state.shopPackages.forEach(p => {
    const el = document.createElement('div');
    el.className = 'shop-item';
    el.innerHTML = `
      ${p.badge ? `<div class="badge">${escapeHtml(p.badge)}</div>` : ''}
      ${p.bonus_percent ? `<div class="bonus">+${p.bonus_percent}%</div>` : ''}
      <div class="icon-box">💗</div>
      <div class="amount">❤️ ${p.hearts_amount}</div>
      <button class="buy-btn" data-id="${p.id}">⭐ ${p.stars_price}</button>
    `;
    el.querySelector('.buy-btn').addEventListener('click', () => buyPackage(p));
    grid.appendChild(el);
  });
}

function buyPackage(pkg) {
  // Telegram Stars orqali to'lov (agar mavjud bo'lsa) - aks holda demo xabar
  if (tg && tg.openInvoice) {
    toast('To\'lov tizimini serverda sozlang (createInvoiceLink). Demo rejimda hearts qo\'shilmoqda.');
  }
  toast(`Demo: ❤️ ${pkg.hearts_amount} paketi tanlandi. To'lov backendni ulang.`);
}

function renderFreeLabels() {
  document.getElementById('inviteBonusLabel').textContent = state.settings.referral_bonus || 20;
  document.getElementById('complimentBonusLabel').textContent = state.settings.compliment_bonus || 10;
  document.getElementById('claimAmount').textContent = state.settings.subscribe_bonus || 5;
}

document.getElementById('inviteFriendBtn').addEventListener('click', shareInviteLink);
document.getElementById('settingsInvite').addEventListener('click', shareInviteLink);
document.getElementById('freeInviteBtn').addEventListener('click', shareInviteLink);

function shareInviteLink() {
  const link = `https://t.me/spinthe_bot?start=ref${state.me.id}`;
  if (tg && tg.openTelegramLink) {
    tg.openTelegramLink(`https://t.me/share/url?url=${encodeURIComponent(link)}&text=${encodeURIComponent('Keling, Spin the Bottle o\'ynaymiz! 🍾❤️')}`);
  } else {
    navigator.clipboard?.writeText(link);
    toast('Havola nusxalandi: ' + link);
  }
}

document.getElementById('complimentBtn').addEventListener('click', async () => {
  try {
    const r = await api('/api/claim-free-hearts?kind=compliment', { method: 'POST' });
    toast(`+${r.bonus} ❤️ qo'shildi!`);
    refreshHearts();
  } catch (e) { toast(e.message); }
});

document.getElementById('freeSubBtn').addEventListener('click', () => {
  const channel = state.settings.required_channel || '@spinthe_channel';
  const link = `https://t.me/${channel.replace('@', '')}`;
  if (tg && tg.openTelegramLink) tg.openTelegramLink(link); else window.open(link, '_blank');
});

document.getElementById('claimFreeBtn').addEventListener('click', async () => {
  try {
    const r = await api('/api/claim-free-hearts?kind=subscribe', { method: 'POST' });
    toast(`+${r.bonus} ❤️ qo'shildi!`);
    refreshHearts();
  } catch (e) { toast(e.message); }
});

// ------------------------------------------------------------------
// BAXT G'ILDIRAGI (Wheel of Fortune)
// ------------------------------------------------------------------
function renderWheel() {
  const svg = document.getElementById('wheelSvg');
  svg.innerHTML = '';
  const prizes = state.wheelPrizes;
  const n = prizes.length || 1;
  const cx = 150, cy = 150, r = 145;
  const anglePer = 360 / n;
  prizes.forEach((p, i) => {
    const start = i * anglePer;
    const end = start + anglePer;
    const path = describeSlice(cx, cy, r, start, end);
    const slice = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    slice.setAttribute('d', path);
    slice.setAttribute('fill', p.color || '#2ecc71');
    slice.setAttribute('stroke', '#ffffff55');
    svg.appendChild(slice);

    const mid = (start + end) / 2;
    const tx = cx + (r * 0.62) * Math.cos((mid - 90) * Math.PI / 180);
    const ty = cy + (r * 0.62) * Math.sin((mid - 90) * Math.PI / 180);
    const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    text.setAttribute('x', tx); text.setAttribute('y', ty);
    text.setAttribute('text-anchor', 'middle');
    text.setAttribute('font-size', '15');
    text.setAttribute('font-weight', '700');
    text.setAttribute('fill', '#ffffff');
    text.setAttribute('transform', `rotate(${mid}, ${tx}, ${ty})`);
    text.textContent = `${p.icon || ''}${p.label}`;
    svg.appendChild(text);
  });
  document.getElementById('chancesBadge').textContent = '🎲 ' + (state.me ? state.me.spins : 0);
  document.getElementById('wheelCost').textContent = state.settings.wheel_spin_cost || 1;
}

function describeSlice(cx, cy, r, startAngle, endAngle) {
  const toRad = (a) => (a - 90) * Math.PI / 180;
  const x1 = cx + r * Math.cos(toRad(startAngle));
  const y1 = cy + r * Math.sin(toRad(startAngle));
  const x2 = cx + r * Math.cos(toRad(endAngle));
  const y2 = cy + r * Math.sin(toRad(endAngle));
  const largeArc = endAngle - startAngle > 180 ? 1 : 0;
  return `M ${cx} ${cy} L ${x1} ${y1} A ${r} ${r} 0 ${largeArc} 1 ${x2} ${y2} Z`;
}

document.getElementById('spinWheelBtn').addEventListener('click', async () => {
  const svg = document.getElementById('wheelSvg');
  try {
    const { prize } = await api('/api/spin-wheel', { method: 'POST' });
    const prizes = state.wheelPrizes;
    const idx = prizes.findIndex(p => p.id === prize.id);
    const anglePer = 360 / (prizes.length || 1);
    const targetMid = idx * anglePer + anglePer / 2;
    const spins = 6;
    const finalRotation = spins * 360 + (360 - targetMid);
    svg.style.transition = 'none';
    svg.style.transform = 'rotate(0deg)';
    void svg.offsetWidth;
    svg.style.transition = 'transform 3.2s cubic-bezier(.12,.67,.15,1)';
    svg.style.transform = `rotate(${finalRotation}deg)`;

    setTimeout(() => {
      document.getElementById('wheelWinnerBanner').innerHTML =
        `🎉 Tabriklaymiz! Siz yutdingiz: <b>${prize.icon}${prize.label}</b>`;
      toast(`Siz ${prize.hearts_reward} ❤️ yutdingiz!`);
      refreshHearts();
      renderWheel();
    }, 3300);
  } catch (e) { toast(e.message); }
});

document.getElementById('chancesPlus').addEventListener('click', () => openModal('shopModal'));

// ------------------------------------------------------------------
// SOVG'A YUBORISH (gift picker)
// ------------------------------------------------------------------
function openGiftModal(preselectedUserId) {
  if (!state.room) return;
  state.selectedTarget = preselectedUserId || (state.room.users.find(u => u.id !== state.me.id) || {}).id;
  renderTargetRow();
  renderGiftGrid();
  openModal('giftModal');
}

function renderTargetRow() {
  const row = document.getElementById('targetRow');
  row.innerHTML = '';
  state.room.users.filter(u => u.id !== state.me.id).forEach(u => {
    const chip = document.createElement('div');
    chip.className = 'target-chip' + (u.id === state.selectedTarget ? ' selected' : '');
    chip.innerHTML = `<img src="${u.photo_url || fallbackAvatar(u)}"><span>${escapeHtml(u.first_name || '')}</span>`;
    chip.addEventListener('click', () => { state.selectedTarget = u.id; renderTargetRow(); });
    row.appendChild(chip);
  });
}

function renderGiftGrid() {
  const grid = document.getElementById('giftGrid');
  grid.innerHTML = '';
  state.reactions.forEach(r => {
    const el = document.createElement('div');
    el.className = 'gift-item';
    el.innerHTML = `<div class="emoji">${r.emoji}</div><div class="cost">❤️ ${r.cost}</div>`;
    el.addEventListener('click', () => sendReaction(r.id));
    grid.appendChild(el);
  });
}

async function sendReaction(reactionId) {
  if (!state.selectedTarget) { toast('Avval qabul qiluvchini tanlang'); return; }
  try {
    await api('/api/send-reaction', { method: 'POST', body: { reaction_id: reactionId, target_user_id: state.selectedTarget } });
    toast('Yuborildi! 🎉');
    closeModal('giftModal');
    refreshHearts();
    loadChat();
  } catch (e) { toast(e.message); }
}

// ------------------------------------------------------------------
// SETTINGS
// ------------------------------------------------------------------
document.getElementById('soundToggle').addEventListener('change', (e) => {
  localStorage.setItem('sound_enabled', e.target.checked ? '1' : '0');
});
document.getElementById('musicToggle').addEventListener('change', (e) => {
  localStorage.setItem('music_enabled', e.target.checked ? '1' : '0');
});
document.getElementById('settingsContact').addEventListener('click', () => {
  const link = 'https://t.me/spinthe_bot';
  if (tg && tg.openTelegramLink) tg.openTelegramLink(link); else window.open(link, '_blank');
});
document.getElementById('settingsProfile').addEventListener('click', () => {
  toast('Profil sozlamalari Telegram profilingiz orqali boshqariladi.');
});

init();
