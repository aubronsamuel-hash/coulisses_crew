const request = require('supertest');
const { app } = require('../server');

const adminHeaders = { 'x-user-role': 'admin' };

beforeEach(async () => {
  await request(app).post('/admin/reset').set(adminHeaders);
});

test('admin_list_get_put_delete_ok', async () => {
  const list = await request(app).get('/admin/users').set(adminHeaders);
  expect(list.status).toBe(200);
  expect(list.body.users.length).toBeGreaterThan(0);

  const user = await request(app).get('/admin/users/2').set(adminHeaders);
  expect(user.status).toBe(200);
  expect(user.body.username).toBe('alice');

  const put = await request(app)
    .put('/admin/users/2')
    .set(adminHeaders)
    .send({ role: 'moderator', is_active: false });
  expect(put.status).toBe(200);
  expect(put.body.role).toBe('moderator');
  expect(put.body.is_active).toBe(false);

  const del = await request(app).delete('/admin/users/2').set(adminHeaders);
  expect(del.status).toBe(204);

  const list2 = await request(app).get('/admin/users').set(adminHeaders);
  expect(list2.body.users.find(u => u.id === 2)).toBeUndefined();
});

test('non_admin_forbidden', async () => {
  const headers = { 'x-user-role': 'user' };
  const list = await request(app).get('/admin/users').set(headers);
  expect(list.status).toBe(403);

  const get = await request(app).get('/admin/users/1').set(headers);
  expect(get.status).toBe(403);

  const put = await request(app).put('/admin/users/1').set(headers).send({ role: 'user' });
  expect(put.status).toBe(403);

  const del = await request(app).delete('/admin/users/1').set(headers);
  expect(del.status).toBe(403);

  const reset = await request(app).post('/admin/reset').set(headers);
  expect(reset.status).toBe(403);
});
