import { getToken, clearToken } from './auth';
import axios from 'axios';
import type { Priority, Ticket, TicketCreate, TicketStatus, TicketUpdate, DashboardSummary } from '../types';

const http = axios.create({
  baseURL: (import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000').replace(/\/$/, ''),
  timeout: 10000,
});

http.interceptors.request.use(config => {
  const token = getToken();
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});
http.interceptors.response.use(response => response, error => {
  if (axios.isAxiosError(error) && error.response?.status === 401 && getToken()) {
    clearToken();
    // A página será redirecionada ao login e o contexto será reiniciado.
    window.location.assign('/login');
  }
  return Promise.reject(error);
});

export interface TicketFilters {
  search?: string;
  status?: TicketStatus;
  priority?: Priority;
}

export const ticketsApi = {
  async list(limit = 20, offset = 0, filters: TicketFilters = {}): Promise<Ticket[]> {
    const { data } = await http.get<Ticket[]>('/api/v1/tickets', {
      params: { limit, offset, ...filters },
    });
    return data;
  },
  async get(id: string): Promise<Ticket> {
    const { data } = await http.get<Ticket>(`/api/v1/tickets/${id}`);
    return data;
  },
  async create(payload: TicketCreate): Promise<Ticket> {
    const { data } = await http.post<Ticket>('/api/v1/tickets', payload);
    return data;
  },
  async update(id: string, payload: TicketUpdate): Promise<Ticket> {
    const { data } = await http.patch<Ticket>(`/api/v1/tickets/${id}`, payload);
    return data;
  },
  async assign(id: string, assigneeId: string | null): Promise<Ticket> {
    const { data } = await http.patch<Ticket>(`/api/v1/tickets/${id}/assignee`, { assignee_id: assigneeId });
    return data;
  },
  async changeStatus(id: string, status: TicketStatus): Promise<Ticket> {
    const { data } = await http.patch<Ticket>(`/api/v1/tickets/${id}/status`, { status });
    return data;
  },
};

export function errorMessage(error: unknown): string {
  if (axios.isAxiosError(error)) {
    if (error.code === 'ECONNABORTED') return 'A API demorou para responder. Tente novamente.';
    if (!error.response) return 'Não foi possível conectar à API. Verifique se o FastAPI está rodando.';
    if (error.response.status >= 500) return 'O servidor encontrou um problema. Tente novamente mais tarde.';
    if (error.response.status === 403) return 'Você não tem permissão para esta operação.';
    if (error.response.status === 404) return 'Chamado não encontrado.';
    if (error.response.status === 409) return 'Operação não permitida. Confira o status ou o responsável selecionado.';
    if (error.response.status === 422) return 'Dados inválidos. Revise os campos preenchidos.';
  }
  return 'Ocorreu um erro inesperado. Tente novamente.';
}

export interface Agent { id: string; name: string; email: string; role: "agent" }
export const agentsApi = {
  async list(): Promise<Agent[]> {
    const { data } = await http.get<Agent[]>("/api/v1/agents");
    return data;
  },
};

export const dashboardApi = {
  async summary(): Promise<DashboardSummary> {
    const { data } = await http.get<DashboardSummary>('/api/v1/dashboard/summary');
    return data;
  },
};

/** Triagem simulada da Sprint 16. Sugestões não são persistidas automaticamente. */
export interface AITriageSuggestion {
  priority: Priority;
  category: 'access' | 'infrastructure' | 'software' | 'hardware' | 'general';
  reason: string;
  provider: string;
}

export const aiTriageApi = {
  async suggest(title: string, description: string): Promise<AITriageSuggestion> {
    const { data } = await http.post<AITriageSuggestion>('/api/v1/ai/triage', {
      title: title.trim(),
      description: description.trim(),
    });
    return data;
  },
};

/** Rascunho de resposta: nunca é publicado automaticamente. */
export interface AIReplySuggestion {
  suggestion: string;
  provider: string;
}

export const aiReplyApi = {
  async suggest(title: string, description: string): Promise<AIReplySuggestion> {
    const { data } = await http.post<AIReplySuggestion>('/api/v1/ai/reply-suggestion', {
      title: title.trim(),
      description: description.trim(),
    });
    return data;
  },
};
