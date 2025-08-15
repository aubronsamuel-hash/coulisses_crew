import { apiFetch } from '../lib/api';

export function list(token: string) {
  return apiFetch('/missions', {
    headers: { Authorization: `Bearer ${token}` }
  });
}

export function create(token: string, mission: Record<string, unknown>) {
  return apiFetch('/missions', {
    method: 'POST',
    body: JSON.stringify(mission),
    headers: { Authorization: `Bearer ${token}` }
  });
}

export function update(token: string, id: number, mission: Record<string, unknown>) {
  return apiFetch(`/missions/${id}`, {
    method: 'PUT',
    body: JSON.stringify(mission),
    headers: { Authorization: `Bearer ${token}` }
  });
}

export function remove(token: string, id: number) {
  return apiFetch(`/missions/${id}`, {
    method: 'DELETE',
    headers: { Authorization: `Bearer ${token}` }
  });
}

export function assign(token: string, id: number, userId: number) {
  return apiFetch(`/missions/${id}/assign`, {
    method: 'POST',
    body: JSON.stringify({ user_id: userId }),
    headers: { Authorization: `Bearer ${token}` }
  });
}
