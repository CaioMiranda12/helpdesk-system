import axios from 'axios';
import type { Ticket, TicketCreate, TicketStatus, TicketUpdate } from '../types';

const http = axios.create({
  baseURL: (import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000').replace(/\/$/, ''),
  timeout: 10000,
});

export const ticketsApi = {
  async list(limit = 20, offset = 0): Promise<Ticket[]> {
    const { data } = await http.get<Ticket[]>('/api/v1/tickets', { params: { limit, offset } });
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
    if (error.response.status === 404) return 'Chamado não encontrado.';
    if (error.response.status === 409) return 'Esta mudança de status não é permitida.';
    if (error.response.status === 422) return 'Dados inválidos. Revise os campos preenchidos.';
  }
  return 'Ocorreu um erro inesperado. Tente novamente.';
}
