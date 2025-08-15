import { apiFetch } from '../lib/api';

export interface LoginRequest {
  username: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
}

export function login(data: LoginRequest): Promise<TokenResponse> {
  return apiFetch('/auth/token-json', {
    method: 'POST',
    body: JSON.stringify(data)
  });
}

export function me(token: string) {
  return apiFetch('/auth/me', {
    headers: { Authorization: `Bearer ${token}` }
  });
}

export function prefs(token: string, prefs: Record<string, unknown>) {
  return apiFetch('/auth/me/prefs', {
    method: 'PUT',
    body: JSON.stringify(prefs),
    headers: { Authorization: `Bearer ${token}` }
  });
}
