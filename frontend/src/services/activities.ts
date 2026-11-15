import axios from 'axios';
import { getToken } from './auth';

export interface TicketActivity {
  id: string;
  ticket_id: string;
  kind: 'comment' | 'status' | 'assignment';
  body: string | null;
  old_value: string | null;
  new_value: string | null;
  author: { id: string; name: string };
  created_at: string;
}
export const ACTIVITY_PAGE_SIZE = 10;
const http = axios.create({ baseURL: (import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000').replace(/\/$/, ''), timeout: 10000 });
http.interceptors.request.use(config => {
  const token = getToken();
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});
export const activitiesApi = {
  async list(ticketId: string, offset = 0, limit = ACTIVITY_PAGE_SIZE + 1): Promise<TicketActivity[]> {
    const { data } = await http.get<TicketActivity[]>(`/api/v1/tickets/${ticketId}/activities`, { params: { limit, offset } });
    return data;
  },
  async comment(ticketId: string, body: string): Promise<TicketActivity> {
    const { data } = await http.post<TicketActivity>(`/api/v1/tickets/${ticketId}/comments`, { body });
    return data;
  },
};

/** Resumo gerado sob demanda; não altera atividades. */
export interface AIActivitySummary {
  summary: string;
  provider: string;
  activities_considered: number;
}

export const aiActivitySummaryApi = {
  async summarize(ticketId: string): Promise<AIActivitySummary> {
    const { data } = await http.post<AIActivitySummary>(
      `/api/v1/tickets/${ticketId}/activities/ai-summary`
    );
    return data;
  },
};
