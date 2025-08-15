export const baseURL = import.meta.env.VITE_API_URL;

export async function apiFetch(path: string, options: RequestInit = {}) {
  const url = `${baseURL}${path}`;
  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {})
  } as Record<string, string>;
  const resp = await fetch(url, { ...options, headers });
  if (!resp.ok) {
    const text = await resp.text();
    throw new Error(`API request failed: ${resp.status} ${text}`);
  }
  if (resp.status === 204) return null;
  return resp.json();
}
