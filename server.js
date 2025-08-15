const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();
app.use(express.json());

const DATA_FILE = path.join(__dirname, 'data.json');

function loadData() {
  if (!fs.existsSync(DATA_FILE)) {
    return { users: [] };
  }
  const raw = fs.readFileSync(DATA_FILE, 'utf-8');
  try {
    return JSON.parse(raw);
  } catch (e) {
    return { users: [] };
  }
}

function saveData(data) {
  fs.writeFileSync(DATA_FILE, JSON.stringify(data, null, 2));
}

const initialData = loadData();

function requireAdmin(req, res, next) {
  const role = req.headers['x-user-role'];
  if (role !== 'admin') {
    return res.status(403).json({ error: 'forbidden' });
  }
  next();
}

app.use(express.static(path.join(__dirname, 'public')));

app.get('/admin/users', requireAdmin, (req, res) => {
  const { q = '', page = '1', per_page = '10' } = req.query;
  const p = parseInt(page, 10);
  const pp = parseInt(per_page, 10);
  const data = loadData();
  const filtered = data.users.filter(u => !u.deleted_at && u.username.includes(q));
  const start = (p - 1) * pp;
  const users = filtered.slice(start, start + pp);
  res.json({ users, total: filtered.length });
});

app.get('/admin/users/:id', requireAdmin, (req, res) => {
  const data = loadData();
  const user = data.users.find(u => u.id === parseInt(req.params.id) && !u.deleted_at);
  if (!user) return res.status(404).end();
  res.json(user);
});

app.put('/admin/users/:id', requireAdmin, (req, res) => {
  const data = loadData();
  const user = data.users.find(u => u.id === parseInt(req.params.id) && !u.deleted_at);
  if (!user) return res.status(404).end();
  const { role, is_active } = req.body;
  if (role !== undefined) user.role = role;
  if (is_active !== undefined) user.is_active = is_active;
  saveData(data);
  res.json(user);
});

app.delete('/admin/users/:id', requireAdmin, (req, res) => {
  const data = loadData();
  const user = data.users.find(u => u.id === parseInt(req.params.id) && !u.deleted_at);
  if (!user) return res.status(404).end();
  user.deleted_at = new Date().toISOString();
  saveData(data);
  res.status(204).end();
});

app.post('/admin/reset', requireAdmin, (req, res) => {
  saveData(initialData);
  res.json({ ok: true });
});

app.get('/admin/notifications/diagnostic', requireAdmin, (req, res) => {
  console.log('notifications diagnostic');
  res.json({ ok: true });
});

app.post('/admin/notifications/diagnostic/test', requireAdmin, (req, res) => {
  console.log('notifications diagnostic test');
  res.json({ ok: true });
});

module.exports = { app, initialData, loadData, saveData };

if (require.main === module) {
  const PORT = process.env.PORT || 3000;
  app.listen(PORT, () => console.log(`Server listening on ${PORT}`));
}
