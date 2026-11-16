
import { useCallback, useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';

import { dashboardApi, errorMessage } from '../services/api';
import type { DashboardSummary } from '../types';

const statusItems = [
  { key: 'open', label: 'Abertos', className: 'status-open', color: '#64748b' },
  { key: 'in_progress', label: 'Em andamento', className: 'status-in_progress', color: '#f59e0b' },
  { key: 'resolved', label: 'Resolvidos', className: 'status-resolved', color: '#16a34a' },
] as const;

const priorityItems = [
  { key: 'low', label: 'Baixa', className: 'priority-low', color: '#16a34a' },
  { key: 'medium', label: 'Média', className: 'priority-medium', color: '#f59e0b' },
  { key: 'high', label: 'Alta', className: 'priority-high', color: '#dc2626' },
] as const;

export function Dashboard() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const load = useCallback(async () => {
    setLoading(true);
    setError('');

    try {
      setSummary(await dashboardApi.summary());
    } catch (err) {
      setSummary(null);
      setError(errorMessage(err));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void load();
  }, [load]);

  const statusData = summary
    ? statusItems.map((item) => ({
      name: item.label,
      value: summary.by_status[item.key],
      color: item.color,
    }))
    : [];

  const priorityData = summary
    ? priorityItems.map((item) => ({
      name: item.label,
      value: summary.by_priority[item.key],
      color: item.color,
    }))
    : [];

  return (
    <section>
      <div className="page-heading">
        <div>
          <p className="eyebrow">VISÃO GERAL</p>
          <h1>Dashboard</h1>
          <p className="muted">
            Indicadores de todos os chamados cadastrados.
          </p>
        </div>

        <button
          className="button subtle"
          type="button"
          onClick={() => void load()}
          disabled={loading}
        >
          Atualizar
        </button>
      </div>

      {loading && (
        <div className="card state-message" role="status">
          Carregando indicadores...
        </div>
      )}

      {!loading && error && (
        <div className="card state-message" role="alert">
          <p>{error}</p>
          <button
            className="button primary"
            type="button"
            onClick={() => void load()}
          >
            Tentar novamente
          </button>
        </div>
      )}

      {!loading && summary && (
        <>
          <div className="dashboard-metrics">
            <div className="card dashboard-total">
              <span>Total de chamados</span>
              <strong>{summary.total}</strong>
              <Link to="/">Ver chamados</Link>
            </div>

            {statusItems.map((item) => (
              <div className="card dashboard-stat" key={item.key}>
                <span>{item.label}</span>
                <strong>{summary.by_status[item.key]}</strong>
                <span className={`pill ${item.className}`}>
                  {summary.total
                    ? Math.round(
                      (summary.by_status[item.key] / summary.total) * 100
                    )
                    : 0}
                  % do total
                </span>
              </div>
            ))}
          </div>

          {summary.total > 0 && (
            <div className="dashboard-charts">
              <div className="card dashboard-chart-card">
                <h2>Chamados por status</h2>
                <p className="muted">
                  Distribuição dos chamados por situação.
                </p>

                <div
                  className="dashboard-chart"
                  role="img"
                  aria-label="Gráfico de chamados por status"
                >
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie
                        data={statusData}
                        dataKey="value"
                        nameKey="name"
                        innerRadius={65}
                        outerRadius={95}
                        paddingAngle={3}
                      >
                        {statusData.map((item) => (
                          <Cell key={item.name} fill={item.color} />
                        ))}
                      </Pie>
                      <Tooltip />
                    </PieChart>
                  </ResponsiveContainer>
                </div>

                <div className="dashboard-chart-legend">
                  {statusData.map((item) => (
                    <div key={item.name}>
                      <span
                        className="dashboard-legend-dot"
                        style={{ backgroundColor: item.color }}
                      />
                      <span>{item.name}</span>
                      <strong>{item.value}</strong>
                    </div>
                  ))}
                </div>
              </div>

              <div className="card dashboard-chart-card">
                <h2>Chamados por prioridade</h2>
                <p className="muted">
                  Comparação entre os níveis de prioridade.
                </p>

                <div
                  className="dashboard-chart"
                  role="img"
                  aria-label="Gráfico de chamados por prioridade"
                >
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart
                      data={priorityData}
                      margin={{ top: 20, right: 10, left: -20, bottom: 5 }}
                    >
                      <CartesianGrid
                        strokeDasharray="3 3"
                        vertical={false}
                      />
                      <XAxis dataKey="name" />
                      <YAxis allowDecimals={false} />
                      <Tooltip />
                      <Bar
                        dataKey="value"
                        name="Chamados"
                        radius={[6, 6, 0, 0]}
                        maxBarSize={65}
                      >
                        {priorityData.map((item) => (
                          <Cell key={item.name} fill={item.color} />
                        ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </div>
          )}

          {summary.total === 0 && (
            <div className="card empty-state">
              <h2>Ainda não existem chamados</h2>
              <p>
                Cadastre o primeiro chamado para visualizar os indicadores.
              </p>
              <Link className="button primary" to="/tickets/new">
                Criar chamado
              </Link>
            </div>
          )}
        </>
      )}
    </section>
  );
}
