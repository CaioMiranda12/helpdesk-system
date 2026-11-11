import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { TicketForm } from '../components/TicketForm';
import { errorMessage, ticketsApi } from '../services/api';
import type { Ticket, TicketStatus } from '../types';
import { nextStatuses, priorityLabels, statusLabels } from '../types';

export function TicketDetail() {
  const { id } = useParams<{ id: string }>();
  const [ticket, setTicket] = useState<Ticket | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [editing, setEditing] = useState(false);
  const [changing, setChanging] = useState(false);

  useEffect(() => {
    let active = true;
    if (!id) { setError('Identificador inválido.'); setLoading(false); return; }
    ticketsApi.get(id).then(data => { if (active) setTicket(data); }).catch(err => { if (active) setError(errorMessage(err)); }).finally(() => { if (active) setLoading(false); });
    return () => { active = false; };
  }, [id]);

  async function changeStatus(status: TicketStatus) {
    if (!ticket) return;
    setChanging(true); setError('');
    try { setTicket(await ticketsApi.changeStatus(ticket.id, status)); }
    catch (err) { setError(errorMessage(err)); }
    finally { setChanging(false); }
  }

  if (loading) return <p className="state-message">Carregando chamado...</p>;
  if (!ticket) return <><Link className="back-link" to="/">← Voltar aos chamados</Link><p className="alert error" role="alert">{error || 'Chamado não encontrado.'}</p></>;

  return <>
    <Link className="back-link" to="/">← Voltar aos chamados</Link>
    <div className="page-heading"><div><p className="eyebrow">CHAMADO #{ticket.id.slice(0, 8)}</p><h1>{ticket.title}</h1><p className="muted">Criado em {new Date(ticket.created_at).toLocaleString('pt-BR')}</p></div><button className="button subtle" onClick={() => setEditing(!editing)}>{editing ? 'Cancelar edição' : 'Editar chamado'}</button></div>
    {error && <p role="alert" className="alert error">{error}</p>}
    {editing ? <TicketForm key={ticket.id} initial={{ title: ticket.title, description: ticket.description, priority: ticket.priority }} submitLabel="Salvar alterações" onSubmit={async values => { try { setTicket(await ticketsApi.update(ticket.id, values)); setEditing(false); } catch (err) { throw new Error(errorMessage(err)); } }} /> :
      <div className="detail-grid"><section className="card detail-card"><h2>Descrição</h2><p className="description">{ticket.description}</p></section><aside className="card detail-card"><h2>Informações</h2><div className="detail-row"><span>Prioridade</span><span className={`pill priority-${ticket.priority}`}>{priorityLabels[ticket.priority]}</span></div><div className="detail-row"><span>Status</span><span className={`pill status-${ticket.status}`}>{statusLabels[ticket.status]}</span></div><div className="detail-row"><span>Atualizado</span><strong>{new Date(ticket.updated_at).toLocaleString('pt-BR')}</strong></div><div className="status-actions"><h3>Próxima etapa</h3>{nextStatuses[ticket.status].map(status => <button key={status} className="button primary" disabled={changing} onClick={() => changeStatus(status)}>{changing ? 'Atualizando...' : `Mover para: ${statusLabels[status]}`}</button>)}</div></aside></div>}
  </>;
}
