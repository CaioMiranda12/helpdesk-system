import { useCallback, useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { dashboardApi, errorMessage } from '../services/api';
import type { DashboardSummary } from '../types';

const statusItems = [
  { key: 'open', label: 'Abertos', className: 'status-open' },
  { key: 'in_progress', label: 'Em andamento', className: 'status-in_progress' },
  { key: 'resolved', label: 'Resolvidos', className: 'status-resolved' },
] as const;
const priorityItems = [
  { key: 'low', label: 'Baixa', className: 'priority-low' },
  { key: 'medium', label: 'Média', className: 'priority-medium' },
  { key: 'high', label: 'Alta', className: 'priority-high' },
] as const;

export function Dashboard() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const load = useCallback(async () => {
    setLoading(true);
    setError('');
    try { setSummary(await dashboardApi.summary()); }
    catch (err) { setSummary(null); setError(errorMessage(err)); }
    finally { setLoading(false); }
  }, []);

  useEffect(() => { void load(); }, [load]);

  return (
    <section>
      <div className="page-heading">
        <div><p className="eyebrow">VISÃO GERAL</p><h1>Dashboard</h1><p className="muted">Indicadores de todos os chamados cadastrados.</p></div>
        <button className="button subtle" type="button" onClick={() => void load()} disabled={loading}>Atualizar</button>
      </div>
      {loading && <div className="card state-message" role="status">Carregando indicadores...</div>}
      {!loading && error && <div className="card state-message" role="alert"><p>{error}</p><button className="button primary" type="button" onClick={() => void load()}>Tentar novamente</button></div>}
      {!loading && summary && <>
        <div className="dashboard-metrics">
          <div className="card dashboard-total"><span>Total de chamados</span><strong>{summary.total}</strong><Link to="/">Ver chamados</Link></div>
          {statusItems.map(item => <div className="card dashboard-stat" key={item.key}><span>{item.label}</span><strong>{summary.by_status[item.key]}</strong><span className={`pill ${item.className}`}>{summary.total ? Math.round(summary.by_status[item.key] / summary.total * 100) : 0}% do total</span></div>)}
        </div>
        <div className="card dashboard-breakdown">
          <h2>Chamados por prioridade</h2>
          {priorityItems.map(item => {
            const count = summary.by_priority[item.key];
            const percent = summary.total ? (count / summary.total) * 100 : 0;
            return <div className="priority-row" key={item.key}>
              <div className="priority-label"><span className={`pill ${item.className}`}>{item.label}</span><strong>{count}</strong></div>
              <div className="priority-track" role="progressbar" aria-label={`Prioridade ${item.label}`} aria-valuenow={count} aria-valuemin={0} aria-valuemax={summary.total || 1}><div className={`priority-fill ${item.key}`} style={{ width: `${percent}%` }} /></div>
            </div>;
          })}
        </div>
        {summary.total === 0 && <div className="card empty-state"><h2>Ainda não existem chamados</h2><p>Cadastre o primeiro chamado para visualizar os indicadores.</p><Link className="button primary" to="/tickets/new">Criar chamado</Link></div>}
      </>}
    </section>
  );
}
