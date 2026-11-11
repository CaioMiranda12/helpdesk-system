import { useEffect, useState } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { errorMessage, ticketsApi } from '../services/api';
import type { Priority, Ticket, TicketStatus } from '../types';
import { priorityLabels, statusLabels } from '../types';

const PAGE_SIZE = 10;
const validStatuses: TicketStatus[] = ['open', 'in_progress', 'resolved'];
const validPriorities: Priority[] = ['low', 'medium', 'high'];

export function TicketList() {
  const [params, setParams] = useSearchParams();
  const search = params.get('search') ?? '';
  const status = params.get('status') ?? '';
  const priority = params.get('priority') ?? '';
  const parsedPage = Number(params.get('page') ?? '1');
  const page = Number.isSafeInteger(parsedPage) && parsedPage > 0 ? parsedPage - 1 : 0;
  const [draftSearch, setDraftSearch] = useState(search);
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [reload, setReload] = useState(0);
  const [hasNextPage, setHasNextPage] = useState(false);
  const filtersActive = Boolean(search || status || priority);

  useEffect(() => { setDraftSearch(search); }, [search]);

  useEffect(() => {
    let active = true;
    setLoading(true);
    setError('');
    ticketsApi.list(PAGE_SIZE + 1, page * PAGE_SIZE, {
      ...(search.trim() ? { search: search.trim() } : {}),
      ...(validStatuses.includes(status as TicketStatus) ? { status: status as TicketStatus } : {}),
      ...(validPriorities.includes(priority as Priority) ? { priority: priority as Priority } : {}),
    })
      .then(data => { if (active) { setTickets(data.slice(0, PAGE_SIZE)); setHasNextPage(data.length > PAGE_SIZE); } })
      .catch(err => { if (active) { setError(errorMessage(err)); setHasNextPage(false); } })
      .finally(() => { if (active) setLoading(false); });
    return () => { active = false; };
  }, [page, search, status, priority, reload]);

  function updateFilters(changes: Record<string, string>) {
    const next = new URLSearchParams(params);
    Object.entries(changes).forEach(([key, value]) => value ? next.set(key, value) : next.delete(key));
    next.delete('page');
    setParams(next);
  }
  function goToPage(nextPage: number) {
    const next = new URLSearchParams(params);
    if (nextPage === 0) next.delete('page'); else next.set('page', String(nextPage + 1));
    setParams(next);
  }
  function retry() { setReload(value => value + 1); }
  function clearFilters() { setDraftSearch(''); setParams(new URLSearchParams()); }

  return (
    <>
      <div className="page-heading"><div><p className="eyebrow">VISÃO GERAL</p><h1>Chamados</h1><p className="muted">Pesquise e acompanhe as solicitações registradas.</p></div><Link className="button primary" to="/tickets/new">+ Novo chamado</Link></div>
      <section className="card filters-card" aria-label="Filtros de chamados">
        <form className="filters-grid" onSubmit={event => { event.preventDefault(); updateFilters({ search: draftSearch.trim() }); }}>
          <label className="filter-field">Pesquisar título<input aria-label="Pesquisar título" type="search" value={draftSearch} maxLength={120} placeholder="Ex.: relatório" onChange={event => setDraftSearch(event.target.value)} /></label>
          <label className="filter-field">Status<select aria-label="Filtrar por status" value={status} onChange={event => updateFilters({ status: event.target.value })}><option value="">Todos</option>{validStatuses.map(value => <option key={value} value={value}>{statusLabels[value]}</option>)}</select></label>
          <label className="filter-field">Prioridade<select aria-label="Filtrar por prioridade" value={priority} onChange={event => updateFilters({ priority: event.target.value })}><option value="">Todas</option>{validPriorities.map(value => <option key={value} value={value}>{priorityLabels[value]}</option>)}</select></label>
          <button className="button primary" type="submit">Pesquisar</button>
          <button className="button subtle" type="button" onClick={clearFilters} disabled={!filtersActive && !draftSearch}>Limpar filtros</button>
        </form>
      </section>
      <section className="card table-card" aria-label="Lista de chamados">
        {loading ? <p className="state-message">Carregando chamados...</p> : error ? <div className="state-message error" role="alert"><p>{error}</p><button className="button subtle" onClick={retry}>Tentar novamente</button></div> : tickets.length === 0 ? <div className="empty-state"><h2>{filtersActive ? 'Nenhum chamado encontrado' : 'Nenhum chamado nesta página'}</h2><p>{filtersActive ? 'Experimente ajustar ou limpar os filtros.' : 'Crie um chamado para começar ou volte à página anterior.'}</p>{filtersActive ? <button className="button subtle" onClick={clearFilters}>Limpar filtros</button> : <Link to="/tickets/new" className="button primary">Criar chamado</Link>}</div> :
          <div className="table-scroll"><table><thead><tr><th>Chamado</th><th>Prioridade</th><th>Status</th><th>Criado em</th></tr></thead><tbody>{tickets.map(ticket => <tr key={ticket.id}><td><Link className="ticket-link" to={`/tickets/${ticket.id}`}>{ticket.title}</Link><span className="ticket-id">#{ticket.id.slice(0, 8)}</span></td><td><span className={`pill priority-${ticket.priority}`}>{priorityLabels[ticket.priority]}</span></td><td><span className={`pill status-${ticket.status}`}>{statusLabels[ticket.status]}</span></td><td className="date">{new Date(ticket.created_at).toLocaleDateString('pt-BR')}</td></tr>)}</tbody></table></div>}
        <div className="pagination"><span>Página {page + 1}</span><div><button className="button subtle" disabled={page === 0 || loading} onClick={() => goToPage(page - 1)}>Anterior</button><button className="button subtle" disabled={loading || !hasNextPage} onClick={() => goToPage(page + 1)}>Próxima</button></div></div>
      </section>
      <p className="hint">A pesquisa e os filtros são aplicados no banco de dados antes da paginação.</p>
    </>
  );
}
