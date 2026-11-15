import { useEffect, useRef, useState } from 'react';
import { aiReplyApi, errorMessage } from '../services/api';

interface Props { title: string; description: string }

export function AIReplyPanel({ title, description }: Props) {
  const [draft, setDraft] = useState('');
  const [hasSuggestion, setHasSuggestion] = useState(false);
  const [provider, setProvider] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [notice, setNotice] = useState('');
  const requestId = useRef(0);

  useEffect(() => {
    requestId.current += 1;
    setDraft(''); setHasSuggestion(false); setProvider(''); setError(''); setNotice(''); setLoading(false);
  }, [title, description]);

  async function suggest() {
    const current = ++requestId.current;
    setLoading(true); setError(''); setNotice('');
    try {
      const result = await aiReplyApi.suggest(title, description);
      if (current !== requestId.current) return;
      setDraft(result.suggestion);
      setProvider(result.provider);
      setHasSuggestion(true);
    } catch (err) {
      if (current === requestId.current) setError(errorMessage(err));
    } finally {
      if (current === requestId.current) setLoading(false);
    }
  }

  async function copyDraft() {
    if (!draft.trim()) return;
    try {
      await navigator.clipboard.writeText(draft);
      setNotice('Rascunho copiado. Revise antes de enviar ao solicitante.');
    } catch {
      setError('Não foi possível copiar. Selecione o texto e copie manualmente.');
    }
  }

  return <section className="card detail-card" aria-labelledby="ai-reply-title">
    <h2 id="ai-reply-title">Sugestão de resposta com IA</h2>
    <p className="muted">Gere um rascunho, revise e edite antes de utilizá-lo. Nada será enviado automaticamente.</p>
    <button type="button" className="button primary" disabled={loading} onClick={() => void suggest()}>
      {loading ? 'Gerando resposta...' : 'Sugerir resposta com IA'}
    </button>
    {error && <p className="alert error" role="alert">{error}</p>}
    {hasSuggestion && <div>
      <p className="muted">Provedor: {provider}</p>
      <label htmlFor="ai-reply-draft">Rascunho editável</label>
      <textarea id="ai-reply-draft" rows={9} value={draft} onChange={event => { setDraft(event.target.value); setNotice(''); }} />
      <div>
        <button type="button" className="button subtle" disabled={!draft.trim()} onClick={() => void copyDraft()}>Copiar resposta</button>
      </div>
      {notice && <p role="status">{notice}</p>}
    </div>}
  </section>;
}
