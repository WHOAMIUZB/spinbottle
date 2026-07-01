// =============================================================================
// Spin the Bottle — Admin panel frontend
// =============================================================================
const tg = window.Telegram ? window.Telegram.WebApp : null;
if (tg) { tg.ready(); tg.expand(); }

const initData = tg && tg.initData ? tg.initData : null;
const urlParams = new URLSearchParams(location.search);
const devUserId = urlParams.get('dev_user_id');

let adminSecret = sessionStorage.getItem('admin_secret') || null;

async function adminApi(path, { method = 'GET', body = null } = {}) {
  const headers = { 'Content-Type': 'application/json' };
  let url = path;
  if (initData) headers['X-Init-Data'] = initData;
  if (adminSecret) headers['X-Admin-Secret'] = adminSecret;
  if (!initData && devUserId) url += (path.includes('?') ? '&' : '?') + 'dev_user_id=' + devUserId;

  const res = await fetch(url, { method, headers, body: body ? JSON.stringify(body) : null });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Xatolik' }));
    throw new Error(err.detail || 'Xatolik yuz berdi');
  }
  return res.json();
}

function toast(msg, isError = false) {
  const t = document.getElementById('adminToast');
  t.textContent = msg;
  t.classList.toggle('error', isError);
  t.classList.add('show');
  clearTimeout(toast._t);
  toast._t = setTimeout(() => t.classList.remove('show'), 2500);
}

// ------------------------------------------------------------------
// LOGIN / AUTH
// ------------------------------------------------------------------
async function tryAutoLogin() {
  try {
    await adminApi('/api/admin/check');
    showApp();
  } catch (e) {
    document.getElementById('loginScreen').style.display = 'flex';
  }
}

document.getElementById('loginBtn').addEventListener('click', async () => {
  const val = document.getElementById('secretInput').value.trim();
  if (!val) return;
  adminSecret = val;
  try {
    await adminApi('/api/admin/check');
    sessionStorage.setItem('admin_secret', val);
    showApp();
  } catch (e) {
    document.getElementById('loginError').textContent = 'Parol noto\'g\'ri yoki ruxsat yo\'q';
    adminSecret = null;
  }
});
document.getElementById('secretInput').addEventListener('keydown', (e) => {
  if (e.key === 'Enter') document.getElementById('loginBtn').click();
});

function showApp() {
  document.getElementById('loginScreen').style.display = 'none';
  document.getElementById('adminApp').style.display = 'flex';
  loadDashboard();
}

// ------------------------------------------------------------------
// TABS
// ------------------------------------------------------------------
document.querySelectorAll('.nav-item').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.nav-item').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById('tab-' + btn.dataset.tab).classList.add('active');
    const loaders = {
      dashboard: loadDashboard, users: loadUsers, reactions: loadReactions,
      wheel: loadWheel, shop: loadShop, rooms: loadRooms, settings: loadSettings,
    };
    if (loaders[btn.dataset.tab]) loaders[btn.dataset.tab]();
  });
});

function esc(s) { return (s ?? '').toString().replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c])); }

// ------------------------------------------------------------------
// DASHBOARD
// ------------------------------------------------------------------
async function loadDashboard() {
  try {
    const stats = await adminApi('/api/admin/stats');
    const grid = document.getElementById('statGrid');
    const labels = {
      total_users: "Jami foydalanuvchilar", total_hearts_in_economy: "Aylanmadagi ❤️",
      total_vip: "VIP foydalanuvchilar", new_users_today: "Bugungi yangi",
      wheel_spins_today: "Bugungi g'ildirak", reactions_sent_total: "Jami sovg'alar",
    };
    grid.innerHTML = Object.entries(labels).map(([k, label]) =>
      `<div class="stat-card"><div class="num">${stats[k] ?? 0}</div><div class="label">${label}</div></div>`
    ).join('');

    const txs = await adminApi('/api/admin/transactions');
    document.querySelector('#txTable tbody').innerHTML = txs.map(t => `
      <tr><td>${t.id}</td><td>${t.user_id}</td><td>${esc(t.type)}</td><td>${t.amount}</td>
      <td>${esc(t.description || '')}</td><td>${new Date(t.created_at * 1000).toLocaleString()}</td></tr>
    `).join('');
  } catch (e) { toast(e.message, true); }
}

// ------------------------------------------------------------------
// USERS
// ------------------------------------------------------------------
async function loadUsers(search = '') {
  try {
    const users = await adminApi('/api/admin/users' + (search ? '?search=' + encodeURIComponent(search) : ''));
    document.querySelector('#usersTable tbody').innerHTML = users.map(u => `
      <tr data-id="${u.id}">
        <td>${u.id}</td>
        <td>${esc(u.first_name)}</td>
        <td>${esc(u.username || '-')}</td>
        <td>${u.hearts}</td>
        <td>${u.spins}</td>
        <td>${u.is_vip ? '👑' : '-'}</td>
        <td>${u.is_banned ? '🚫' : '-'}</td>
        <td>
          <input class="mini-input" type="number" placeholder="+/- ❤️" data-delta-hearts>
          <button class="row-btn save" data-action="adjust-hearts">Qo'llash</button><br><br>
          <button class="row-btn toggle" data-action="toggle-vip">${u.is_vip ? 'VIP olib tashlash' : 'VIP berish'}</button>
          <button class="row-btn delete" data-action="toggle-ban">${u.is_banned ? 'Blokdan chiqarish' : 'Bloklash'}</button>
        </td>
      </tr>
    `).join('');

    document.querySelectorAll('#usersTable [data-action]').forEach(btn => {
      btn.addEventListener('click', async () => {
        const tr = btn.closest('tr');
        const id = tr.dataset.id;
        try {
          if (btn.dataset.action === 'adjust-hearts') {
            const delta = parseInt(tr.querySelector('[data-delta-hearts]').value || '0', 10);
            if (!delta) return toast('Miqdorni kiriting', true);
            await adminApi(`/api/admin/users/${id}`, { method: 'POST', body: { hearts_delta: delta } });
          } else if (btn.dataset.action === 'toggle-vip') {
            const isVip = btn.textContent.includes('olib');
            await adminApi(`/api/admin/users/${id}`, { method: 'POST', body: { is_vip: !isVip } });
          } else if (btn.dataset.action === 'toggle-ban') {
            const isBanned = btn.textContent.includes('chiqarish');
            await adminApi(`/api/admin/users/${id}`, { method: 'POST', body: { is_banned: !isBanned } });
          }
          toast('Saqlandi ✅');
          loadUsers(document.getElementById('userSearch').value);
        } catch (e) { toast(e.message, true); }
      });
    });
  } catch (e) { toast(e.message, true); }
}
let searchTimer;
document.getElementById('userSearch').addEventListener('input', (e) => {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(() => loadUsers(e.target.value), 350);
});

// ------------------------------------------------------------------
// REACTIONS (yangi reaksiya qo'shish + ball belgilash)
// ------------------------------------------------------------------
async function loadReactions() {
  try {
    const items = await adminApi('/api/admin/reactions');
    document.querySelector('#reactionsTable tbody').innerHTML = items.map(r => `
      <tr data-id="${r.id}">
        <td style="font-size:20px">${r.emoji}</td>
        <td>${esc(r.name)}</td>
        <td><input class="mini-input" type="number" value="${r.cost}" data-field="cost"></td>
        <td><input class="mini-input" type="number" value="${r.points}" data-field="points"></td>
        <td>${r.is_active ? '✅' : '❌'}</td>
        <td>
          <button class="row-btn save" data-action="save">Saqlash</button>
          <button class="row-btn toggle" data-action="toggle">${r.is_active ? 'O\'chirish' : 'Yoqish'}</button>
          <button class="row-btn delete" data-action="delete">O'chirib tashlash</button>
        </td>
      </tr>
    `).join('');
    bindCrudRow('#reactionsTable', '/api/admin/reactions');
  } catch (e) { toast(e.message, true); }
}

document.getElementById('reactionForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const f = new FormData(e.target);
  try {
    await adminApi('/api/admin/reactions', {
      method: 'POST',
      body: { emoji: f.get('emoji'), name: f.get('name'), cost: +f.get('cost'), points: +f.get('points') },
    });
    e.target.reset();
    toast('Yangi reaksiya qo\'shildi ✅');
    loadReactions();
  } catch (e2) { toast(e2.message, true); }
});

// ------------------------------------------------------------------
// WHEEL PRIZES
// ------------------------------------------------------------------
async function loadWheel() {
  try {
    const items = await adminApi('/api/admin/wheel-prizes');
    document.querySelector('#wheelTable tbody').innerHTML = items.map(p => `
      <tr data-id="${p.id}">
        <td style="font-size:18px">${p.icon}</td>
        <td><input class="mini-input" value="${esc(p.label)}" data-field="label" style="width:90px"></td>
        <td><input class="mini-input" type="number" value="${p.hearts_reward}" data-field="hearts_reward"></td>
        <td><input class="mini-input" type="number" value="${p.weight}" data-field="weight"></td>
        <td><input type="color" value="${p.color}" data-field="color" style="width:40px"></td>
        <td>${p.is_active ? '✅' : '❌'}</td>
        <td>
          <button class="row-btn save" data-action="save">Saqlash</button>
          <button class="row-btn toggle" data-action="toggle">${p.is_active ? 'O\'chirish' : 'Yoqish'}</button>
          <button class="row-btn delete" data-action="delete">O'chirib tashlash</button>
        </td>
      </tr>
    `).join('');
    bindCrudRow('#wheelTable', '/api/admin/wheel-prizes');
  } catch (e) { toast(e.message, true); }
}

document.getElementById('wheelForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const f = new FormData(e.target);
  try {
    await adminApi('/api/admin/wheel-prizes', {
      method: 'POST',
      body: {
        label: f.get('label'), hearts_reward: +f.get('hearts_reward'),
        weight: +f.get('weight'), icon: f.get('icon') || '❤️', color: f.get('color') || '#2ecc71',
      },
    });
    e.target.reset();
    toast('Yangi sovg\'a qo\'shildi ✅');
    loadWheel();
  } catch (e2) { toast(e2.message, true); }
});

// ------------------------------------------------------------------
// SHOP PACKAGES
// ------------------------------------------------------------------
async function loadShop() {
  try {
    const items = await adminApi('/api/admin/shop-packages');
    document.querySelector('#shopTable tbody').innerHTML = items.map(p => `
      <tr data-id="${p.id}">
        <td><input class="mini-input" type="number" value="${p.hearts_amount}" data-field="hearts_amount"></td>
        <td><input class="mini-input" type="number" value="${p.stars_price}" data-field="stars_price"></td>
        <td><input class="mini-input" type="number" value="${p.bonus_percent}" data-field="bonus_percent"></td>
        <td><input class="mini-input" value="${esc(p.badge || '')}" data-field="badge" style="width:100px"></td>
        <td><input class="mini-input" type="number" value="${p.sort_order}" data-field="sort_order"></td>
        <td>${p.is_active ? '✅' : '❌'}</td>
        <td>
          <button class="row-btn save" data-action="save">Saqlash</button>
          <button class="row-btn toggle" data-action="toggle">${p.is_active ? 'O\'chirish' : 'Yoqish'}</button>
          <button class="row-btn delete" data-action="delete">O'chirib tashlash</button>
        </td>
      </tr>
    `).join('');
    bindCrudRow('#shopTable', '/api/admin/shop-packages');
  } catch (e) { toast(e.message, true); }
}

document.getElementById('shopForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const f = new FormData(e.target);
  try {
    await adminApi('/api/admin/shop-packages', {
      method: 'POST',
      body: {
        hearts_amount: +f.get('hearts_amount'), stars_price: +f.get('stars_price'),
        bonus_percent: +f.get('bonus_percent') || 0, badge: f.get('badge') || null,
        sort_order: +f.get('sort_order') || 0,
      },
    });
    e.target.reset();
    toast('Yangi paket qo\'shildi ✅');
    loadShop();
  } catch (e2) { toast(e2.message, true); }
});

// ------------------------------------------------------------------
// GENERIC CRUD ROW BINDING (reactions/wheel/shop uchun umumiy)
// ------------------------------------------------------------------
function bindCrudRow(tableSel, apiPath) {
  document.querySelectorAll(`${tableSel} [data-action]`).forEach(btn => {
    btn.addEventListener('click', async () => {
      const tr = btn.closest('tr');
      const id = tr.dataset.id;
      try {
        if (btn.dataset.action === 'save') {
          const fields = {};
          tr.querySelectorAll('[data-field]').forEach(inp => {
            const key = inp.dataset.field;
            fields[key] = inp.type === 'number' ? Number(inp.value) : inp.value;
          });
          await adminApi(`${apiPath}/${id}`, { method: 'PUT', body: fields });
          toast('Saqlandi ✅');
        } else if (btn.dataset.action === 'toggle') {
          const isActive = btn.textContent.includes("O'chirish");
          await adminApi(`${apiPath}/${id}`, { method: 'PUT', body: { is_active: !isActive } });
          toast('Holat o\'zgartirildi ✅');
        } else if (btn.dataset.action === 'delete') {
          if (!confirm("Rostdan ham o'chirmoqchimisiz?")) return;
          await adminApi(`${apiPath}/${id}`, { method: 'DELETE' });
          toast("O'chirildi ✅");
        }
        // qayta yuklash
        if (apiPath.includes('reactions')) loadReactions();
        else if (apiPath.includes('wheel')) loadWheel();
        else if (apiPath.includes('shop')) loadShop();
      } catch (e) { toast(e.message, true); }
    });
  });
}

// ------------------------------------------------------------------
// ROOMS
// ------------------------------------------------------------------
async function loadRooms() {
  try {
    const rooms = await adminApi('/api/admin/rooms');
    document.querySelector('#roomsTable tbody').innerHTML = rooms.map(r => `
      <tr><td>${r.id}</td><td>${esc(r.name)}</td><td>${r.seats}</td></tr>
    `).join('');
  } catch (e) { toast(e.message, true); }
}

document.getElementById('roomForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const f = new FormData(e.target);
  try {
    await adminApi('/api/admin/rooms', { method: 'POST', body: { name: f.get('name'), seats: +f.get('seats') } });
    e.target.reset();
    toast('Xona qo\'shildi ✅');
    loadRooms();
  } catch (e2) { toast(e2.message, true); }
});

// ------------------------------------------------------------------
// BROADCAST
// ------------------------------------------------------------------
document.getElementById('broadcastBtn').addEventListener('click', async () => {
  const text = document.getElementById('broadcastText').value.trim();
  if (!text) return toast('Xabar matnini kiriting', true);
  if (!confirm("Xabar barcha foydalanuvchilarga yuboriladi. Davom etasizmi?")) return;
  try {
    document.getElementById('broadcastResult').textContent = 'Yuborilmoqda...';
    const r = await adminApi('/api/admin/broadcast', { method: 'POST', body: { text } });
    document.getElementById('broadcastResult').textContent = `Yuborildi: ${r.sent}/${r.total}`;
    toast('Xabar yuborildi ✅');
  } catch (e) { toast(e.message, true); }
});

// ------------------------------------------------------------------
// SETTINGS
// ------------------------------------------------------------------
const SETTING_LABELS = {
  required_channel: "Majburiy obuna kanali (@...)",
  referral_bonus: "Do'st taklif qilish bonusi (❤️)",
  subscribe_bonus: "Kanalga obuna bonusi (❤️)",
  compliment_bonus: "Kompliment bonusi (❤️)",
  wheel_spin_cost: "G'ildirak aylantirish narxi (chance)",
  game_title: "O'yin nomi",
};

async function loadSettings() {
  try {
    const s = await adminApi('/api/admin/settings');
    const grid = document.getElementById('settingsGrid');
    grid.innerHTML = Object.entries(SETTING_LABELS).map(([key, label]) => `
      <div class="setting-field">
        <label>${label}</label>
        <input data-key="${key}" value="${esc(s[key] ?? '')}">
      </div>
    `).join('');
  } catch (e) { toast(e.message, true); }
}

document.getElementById('saveSettingsBtn').addEventListener('click', async () => {
  const settings = {};
  document.querySelectorAll('#settingsGrid [data-key]').forEach(inp => { settings[inp.dataset.key] = inp.value; });
  try {
    await adminApi('/api/admin/settings', { method: 'POST', body: { settings } });
    toast('Sozlamalar saqlandi ✅');
  } catch (e) { toast(e.message, true); }
});

tryAutoLogin();
