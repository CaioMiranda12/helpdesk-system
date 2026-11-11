import { useEffect, useRef, useState } from 'react';
import { ACTIVITY_PAGE_SIZE, activitiesApi } from '../services/activities';
import type { TicketActivity } from '../services/activities';
import { errorMessage } from '../services/api';
import { statusLabels } from '../types';
import type { TicketStatus } from '../types';

function description(activity: TicketActivity): string {
  if (activity.kind === 'comment') return activity.body || '';
  if (activity.kind === 'status') {
    const before = statusLabels[activity.old_value as TicketStatus] ?? activity.old_value;
    const after = statusLabels[activity.new_value as TicketStatus] ?? activity.new_value;
    return `Alterou o status: ${before} → ${after}`;
  }
  return activity.new_value ? 'Alterou o responsável do chamado' : 'Removeu o responsável do chamado';
}

export function TicketActivityPanel({ ticketId, refreshKey }: { ticketId: string; refreshKey: number }) {
  const [activities, setActivities] = useState<TicketActivity[]>([]);
  const [body, setBody] = useState('');
  const [loading, setLoading] = useState(true);
  const [loadingMore, setLoadingMore] = useState(false);
  const [hasMore, setHasMore] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const generation = useRef(0);
  const offset = useRef(0);
  const busy = useRef(false);

  async function reload() {
    const current = ++generation.current;
    busy.current = false;
    offset.current = 0;
    setLoading(true);
    setHasMore(false);
    setActivities([]);
    setError('');
    try {
      const page = await activitiesApi.list(ticketId);
      if (current !== generation.current) return;
      setActivities(page.slice(0, ACTIVITY_PAGE_SIZE));
      offset.current = Math.min(page.length, ACTIVITY_PAGE_SIZE);
      setHasMore(page.length > ACTIVITY_PAGE_SIZE);
    } catch (err) {
      if (current === generation.current) setError(errorMessage(err));
    } finally {
      if (current === generation.current) setLoading(false);
    }
  }

  useEffect(() => {
    void reload();
    return () => { generation.current += 1; };
  }, [ticketId, refreshKey]);

  async function loadMore() {
    if (busy.current || loading || !hasMore) return;
    busy.current = true;
    const current = generation.current;
    setLoadingMore(true);
    setError('');
    try {
      const page = await activitiesApi.list(ticketId, offset.current);
      if (current !== generation.current) return;
      const items = page.slice(0, ACTIVITY_PAGE_SIZE);
      setActivities(previous => {
        const seen = new Set(previous.map(item => item.id));
        return [...previous, ...items.filter(item => !seen.has(item.id))];
      });
      offset.current += items.length;
      setHasMore(page.length > ACTIVITY_PAGE_SIZE);
    } catch (err) {
      if (current === generation.current) setError(errorMessage(err));
    } finally {
      if (current === generation.current) { setLoadingMore(false); busy.current = false; }
    }
  }

  async function submit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!body.trim() || saving) return;
    setSaving(true);
    try {
      await activitiesApi.comment(ticketId, body.trim());
      setBody('');
      await reload();
    } catch (err) { setError(errorMessage(err)); }
    finally { setSaving(false); }
  }

  return <section className="card detail-card activity-panel">
    <h2>Comentários e histórico</h2>
    <form onSubmit={event => void submit(event)} className="activity-form">
      <label htmlFor="activity-body">Adicionar comentário</label>
      <textarea id="activity-body" value={body} maxLength={2000} rows={3} onChange={event => setBody(event.target.value)} placeholder="Descreva uma atualização do atendimento..." />
      <button className="button primary" type="submit" disabled={saving || !body.trim()}>{saving ? 'Enviando...' : 'Publicar comentário'}</button>
    </form>
    {error && <p role="alert" className="alert error">{error} <button type="button" onClick={() => void reload()}>Tentar novamente</button></p>}
    {loading ? <p role="status">Carregando histórico...</p> : activities.length === 0 ? <p className="muted">Nenhuma atividade registrada ainda.</p> : <>
      <ol className="activity-list">{activities.map(activity => <li key={activity.id} className="activity-item">
        <div><strong>{activity.author.name}</strong> <small className="muted">{new Date(activity.created_at).toLocaleString('pt-BR')}</small></div>
        <p>{description(activity)}</p>
      </li>)}</ol>
      <div className="activity-pagination" aria-live="polite">
        <span className="muted">{activities.length} atividade(s) exibida(s)</span>
        {hasMore && <button type="button" className="button subtle" onClick={() => void loadMore()} disabled={loadingMore}>{loadingMore ? 'Carregando...' : 'Carregar atividades anteriores'}</button>}
      </div>
    </>}
  </section>;
}
