import { getToken } from './auth';
import axios from 'axios';
import type { CurrentUser } from './auth';

const baseURL = (import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000').replace(/\/$/, '');
const client = axios.create({ baseURL, timeout: 10000 });
client.interceptors.request.use(config => {
  const token = getToken();
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export interface CreateUser { name: string; email: string; password: string; role: 'admin' | 'agent' }
export const usersApi = {
  async list(): Promise<CurrentUser[]> {
    const { data } = await client.get<CurrentUser[]>('/api/v1/users', { params: { limit: 100, offset: 0 } });
    return data;
  },
  async create(payload: CreateUser): Promise<CurrentUser> {
    const { data } = await client.post<CurrentUser>('/api/v1/users', payload);
    return data;
  },
};
