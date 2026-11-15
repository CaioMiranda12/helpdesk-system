import { useEffect, useRef, useState } from 'react';
import { aiActivitySummaryApi } from '../services/activities';
import { errorMessage } from '../services/api';

interface Props {
  ticketId: string;
  refreshKey: number;
  hasActivities: boolean;
}

export function AIActivitySummaryPanel({ ticketId, refreshKey, hasActivities }: Props) {
  const [summary, setSummary] = useState('');
  const [provider, setProvider] = useState('');
  const [count, setCount] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const generation = useRef(0);

  useEffect(() => {
    generation.current += 1;
    setSummary('');
    setProvider('');
    setCount(0);
    setError('');
    setLoading(false);
    return () => { generation.current += 1; };
  }, [ticketId, refreshKey]);

  async function generate() {
    const current = ++generation.current;
    setLoading(true);
    setError('');
    setSummary('');
    try {
      const result = await aiActivitySummaryApi.summarize(ticketId);
      if (current !== generation.current) return;
      setSummary(result.summary);
      setProvider(result.provider);
      setCount(result.activities_considered);
    } catch (err) {
      if (current === generation.current) setError(errorMessage(err));
    } finally {
      if (current === generation.current) setLoading(false);
    }
  }

  return <div className="ai-activity-summary" aria-labelledby="ai-activity-summary-title">
    <h3 id="ai-activity-summary-title">Resumo de atividades com IA</h3>
    <p className="muted">O resumo considera até 50 atividades recentes. Confira o histórico antes de tomar decisões; nada será alterado automaticamente.</p>
    <button className="button subtle" type="button" disabled={loading || !hasActivities} onClick={() => void generate()}>
      {loading ? 'Gerando resumo...' : 'Resumir atividades com IA'}
    </button>
    {error && <p role="alert" className="alert error">{error}</p>}
    {summary && <div aria-label="Resumo gerado por IA">
      <p className="muted">Provedor: {provider} · {count} atividade(s) considerada(s)</p>
      <p style={{ whiteSpace: 'pre-wrap' }}>{summary}</p>
    </div>}
  </div>;
}
