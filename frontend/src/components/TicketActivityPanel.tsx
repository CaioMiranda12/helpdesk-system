import { useEffect, useState } from 'react';
import { activitiesApi } from '../services/activities';
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
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  async function reload() {
    try { setActivities(await activitiesApi.list(ticketId)); setError(''); }
    catch (err) { setError(errorMessage(err)); }
    finally { setLoading(false); }
  }
  useEffect(() => { void reload(); }, [ticketId, refreshKey]);
  async function submit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!body.trim() || saving) return;
    setSaving(true);
    try { await activitiesApi.comment(ticketId, body.trim()); setBody(''); await reload(); }
    catch (err) { setError(errorMessage(err)); }
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
    {loading ? <p>Carregando histórico...</p> : activities.length === 0 ? <p className="muted">Nenhuma atividade registrada ainda.</p> :
      <ol className="activity-list">{activities.map(activity => <li key={activity.id} className="activity-item">
        <div><strong>{activity.author.name}</strong> <small className="muted">{new Date(activity.created_at).toLocaleString('pt-BR')}</small></div>
        <p>{description(activity)}</p>
      </li>)}</ol>}
  </section>;
}
