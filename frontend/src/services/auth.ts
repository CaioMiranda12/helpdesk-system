import axios from 'axios';

const BASE_URL = (import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000').replace(/\/$/, '');
export interface CurrentUser { id: string; email: string; name: string; role: 'admin' | 'agent' }
export interface LoginResponse { access_token: string; token_type: string; user: CurrentUser }
const TOKEN_KEY = 'helpdesk_access_token';

export const getToken = () => sessionStorage.getItem(TOKEN_KEY);
export const saveToken = (token: string) => sessionStorage.setItem(TOKEN_KEY, token);
export const clearToken = () => sessionStorage.removeItem(TOKEN_KEY);

export async function login(email: string, password: string): Promise<LoginResponse> {
  const { data } = await axios.post<LoginResponse>(`${BASE_URL}/api/v1/auth/login`, { email, password });
  return data;
}
export async function currentUser(): Promise<CurrentUser> {
  const { data } = await axios.get<CurrentUser>(`${BASE_URL}/api/v1/auth/me`, {
    headers: { Authorization: `Bearer ${getToken()}` }, timeout: 10000,
  });
  return data;
}
