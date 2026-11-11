export type Priority = 'low' | 'medium' | 'high';
export type TicketStatus = 'open' | 'in_progress' | 'resolved';

export interface Ticket {
  id: string;
  title: string;
  description: string;
  priority: Priority;
  status: TicketStatus;
  created_at: string;
  updated_at: string;
}

export interface TicketCreate {
  title: string;
  description: string;
  priority: Priority;
}

export type TicketUpdate = Partial<TicketCreate>;

export const priorityLabels: Record<Priority, string> = {
  low: 'Baixa', medium: 'Média', high: 'Alta',
};
export const statusLabels: Record<TicketStatus, string> = {
  open: 'Aberto', in_progress: 'Em andamento', resolved: 'Resolvido',
};
export const nextStatuses: Record<TicketStatus, TicketStatus[]> = {
  open: ['in_progress'],
  in_progress: ['resolved'],
  resolved: ['in_progress'],
};

export interface DashboardSummary {
  total: number;
  by_status: Record<TicketStatus, number>;
  by_priority: Record<Priority, number>;
}
