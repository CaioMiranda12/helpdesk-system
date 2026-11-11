import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { errorMessage, ticketsApi } from '../services/api';
import type { Ticket } from '../types';
import { priorityLabels, statusLabels } from '../types';

const PAGE_SIZE = 10;
export function TicketList() {
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [page, setPage] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [reload, setReload] = useState(0);
  const [hasNextPage, setHasNextPage] = useState(false);

  useEffect(() => {
    let active = true;
    ticketsApi.list(PAGE_SIZE + 1, page * PAGE_SIZE)
      .then(data => { if (active) { setTickets(data.slice(0, PAGE_SIZE)); setHasNextPage(data.length > PAGE_SIZE); } })
      .catch(err => { if (active) setError(errorMessage(err)); })
      .finally(() => { if (active) setLoading(false); });
    return () => { active = false; };
  }, [page, reload]);

  function goToPage(nextPage: number) { setLoading(true); setError(''); setPage(nextPage); }
  function retry() { setLoading(true); setError(''); setReload(value => value + 1); }

  return (
    <>
      <div className="page-heading"><div><p className="eyebrow">VISÃO GERAL</p><h1>Chamados</h1><p className="muted">Acompanhe as solicitações registradas.</p></div><Link className="button primary" to="/tickets/new">+ Novo chamado</Link></div>
      <section className="card table-card" aria-label="Lista de chamados">
        {loading ? <p className="state-message">Carregando chamados...</p> : error ? <div className="state-message error" role="alert"><p>{error}</p><button className="button subtle" onClick={retry}>Tentar novamente</button></div> : tickets.length === 0 ? <div className="empty-state"><h2>Nenhum chamado nesta página</h2><p>Crie um chamado para começar ou volte à página anterior.</p><Link to="/tickets/new" className="button primary">Criar chamado</Link></div> :
          <div className="table-scroll"><table><thead><tr><th>Chamado</th><th>Prioridade</th><th>Status</th><th>Criado em</th></tr></thead><tbody>{tickets.map(ticket => <tr key={ticket.id}><td><Link className="ticket-link" to={`/tickets/${ticket.id}`}>{ticket.title}</Link><span className="ticket-id">#{ticket.id.slice(0, 8)}</span></td><td><span className={`pill priority-${ticket.priority}`}>{priorityLabels[ticket.priority]}</span></td><td><span className={`pill status-${ticket.status}`}>{statusLabels[ticket.status]}</span></td><td className="date">{new Date(ticket.created_at).toLocaleDateString('pt-BR')}</td></tr>)}</tbody></table></div>}
        <div className="pagination"><span>Página {page + 1}</span><div><button className="button subtle" disabled={page === 0 || loading} onClick={() => goToPage(page - 1)}>Anterior</button><button className="button subtle" disabled={loading || !hasNextPage} onClick={() => goToPage(page + 1)}>Próxima</button></div></div>
      </section>
      <p className="hint">A API retorna até {PAGE_SIZE} chamados por página. A próxima página só fica disponível quando há mais registros.</p>
    </>
  );
}
