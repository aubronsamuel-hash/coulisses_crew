import { useState, useCallback } from 'react';
import * as authService from '../services/auth';

interface User {
  id: number;
  username: string;
  role: string;
  [key: string]: unknown;
}

export function useAuth() {
  const [token, setToken] = useState<string | null>(null);
  const [user, setUser] = useState<User | null>(null);

  const login = useCallback(async (username: string, password: string) => {
    const { access_token } = await authService.login({ username, password });
    setToken(access_token);
    const me = await authService.me(access_token);
    setUser(me);
  }, []);

  const fetchMe = useCallback(async () => {
    if (!token) return;
    const me = await authService.me(token);
    setUser(me);
  }, [token]);

  const updatePrefs = useCallback(
    async (prefs: Record<string, unknown>) => {
      if (!token) return;
      await authService.prefs(token, prefs);
    },
    [token]
  );

  return { token, user, login, fetchMe, updatePrefs };
}
