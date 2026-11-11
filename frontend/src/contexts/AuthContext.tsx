import { createContext, useContext, useEffect, useState } from 'react';
import type { ReactNode } from 'react';
import { clearToken, currentUser, getToken, login, saveToken } from '../services/auth';
import type { CurrentUser } from '../services/auth';

interface AuthValue {
  user: CurrentUser | null;
  loading: boolean;
  signIn: (email: string, password: string) => Promise<void>;
  signOut: () => void;
}
const AuthContext = createContext<AuthValue | null>(null);
export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<CurrentUser | null>(null);
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    let active = true;
    if (!getToken()) { setLoading(false); return; }
    currentUser().then(value => { if (active) setUser(value); }).catch(() => { clearToken(); }).finally(() => { if (active) setLoading(false); });
    return () => { active = false; };
  }, []);
  async function signIn(email: string, password: string) {
    const response = await login(email, password);
    saveToken(response.access_token);
    setUser(response.user);
  }
  function signOut() { clearToken(); setUser(null); }
  return <AuthContext.Provider value={{ user, loading, signIn, signOut }}>{children}</AuthContext.Provider>;
}
export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error('AuthProvider ausente');
  return context;
}
