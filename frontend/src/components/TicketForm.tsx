import { useState, type FormEvent } from 'react';
import type { Priority, TicketCreate } from '../types';
import { priorityLabels } from '../types';
import { aiTriageApi, errorMessage, type AITriageSuggestion } from '../services/api';

interface Props {
  initial?: TicketCreate;
  submitLabel: string;
  onSubmit: (values: TicketCreate) => Promise<void>;
}

export function TicketForm({ initial, submitLabel, onSubmit }: Props) {
  const [title, setTitle] = useState(initial?.title ?? '');
  const [description, setDescription] = useState(initial?.description ?? '');
  const [priority, setPriority] = useState<Priority>(initial?.priority ?? 'medium');
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [triaging, setTriaging] = useState(false);
  const [triageError, setTriageError] = useState('');
  const [suggestion, setSuggestion] = useState<AITriageSuggestion | null>(null);

  async function handleTriage() {
    const cleanTitle = title.trim();
    const cleanDescription = description.trim();
    if (cleanTitle.length < 5 || cleanDescription.length < 10) {
      setTriageError('Preencha um título com pelo menos 5 caracteres e uma descrição com pelo menos 10.');
      return;
    }
    setTriaging(true);
    setTriageError('');
    setSuggestion(null);
    try {
      setSuggestion(await aiTriageApi.suggest(cleanTitle, cleanDescription));
    } catch (err) {
      setTriageError(errorMessage(err));
    } finally {
      setTriaging(false);
    }
  }

  function applySuggestion() {
    if (!suggestion) return;
    setPriority(suggestion.priority);
    setSuggestion(null);
  }

  function invalidateSuggestion() {
    setSuggestion(null);
    setTriageError('');
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const values = { title: title.trim(), description: description.trim(), priority };
    if (values.title.length < 5 || values.description.length < 10) {
      setError('O título precisa de 5 caracteres e a descrição de 10 caracteres, no mínimo.');
      return;
    }
    setSaving(true);
    setError('');
    try { await onSubmit(values); }
    catch (err) { setError(err instanceof Error ? err.message : 'Não foi possível salvar.'); }
    finally { setSaving(false); }
  }

  return (
    <form className="form card" onSubmit={handleSubmit}>
      <label htmlFor="title">Título <span className="required">*</span></label>
      <input id="title" value={title} onChange={e => { setTitle(e.target.value); invalidateSuggestion(); }} minLength={5} maxLength={120} required placeholder="Ex.: Impressora não está funcionando" />
      <p className="hint">Entre 5 e 120 caracteres.</p>
      <label htmlFor="description">Descrição <span className="required">*</span></label>
      <textarea id="description" value={description} onChange={e => { setDescription(e.target.value); invalidateSuggestion(); }} minLength={10} maxLength={2000} rows={6} required placeholder="Descreva o problema e o comportamento esperado..." />
      <p className="hint">Entre 10 e 2000 caracteres.</p>
      <label htmlFor="priority">Prioridade</label>
      <select id="priority" value={priority} onChange={e => setPriority(e.target.value as Priority)}>
        {(Object.keys(priorityLabels) as Priority[]).map(value => <option key={value} value={value}>{priorityLabels[value]}</option>)}
      </select>
      <div className="form-actions">
        <button className="button" type="button" onClick={handleTriage} disabled={saving || triaging}>
          {triaging ? 'Analisando...' : 'Sugerir triagem'}
        </button>
      </div>
      {triageError && <p role="alert" className="alert error">{triageError}</p>}
      {suggestion && (
        <section aria-label="Sugestão de triagem" className="card">
          <p><strong>Prioridade sugerida:</strong> {priorityLabels[suggestion.priority]}</p>
          <p><strong>Categoria sugerida:</strong> {{ access: 'Acesso', infrastructure: 'Infraestrutura', software: 'Software', hardware: 'Hardware', general: 'Geral' }[suggestion.category]}</p>
          <p><strong>Motivo:</strong> {suggestion.reason}</p>
          <p className="hint">Sugestão automática: pode ser gerada por regras ou por IA, conforme a configuração do servidor. Revise antes de aplicar. A categoria não é salva no chamado.</p>
          <button className="button" type="button" onClick={applySuggestion} disabled={saving}>Aplicar prioridade sugerida</button>
        </section>
      )}
      {error && <p role="alert" className="alert error">{error}</p>}
      <div className="form-actions"><button className="button primary" disabled={saving} type="submit">{saving ? 'Salvando...' : submitLabel}</button></div>
    </form>
  );
}
