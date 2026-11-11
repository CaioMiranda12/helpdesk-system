import { useState, type FormEvent } from 'react';
import type { Priority, TicketCreate } from '../types';
import { priorityLabels } from '../types';

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
      <input id="title" value={title} onChange={e => setTitle(e.target.value)} minLength={5} maxLength={120} required placeholder="Ex.: Impressora não está funcionando" />
      <p className="hint">Entre 5 e 120 caracteres.</p>
      <label htmlFor="description">Descrição <span className="required">*</span></label>
      <textarea id="description" value={description} onChange={e => setDescription(e.target.value)} minLength={10} maxLength={2000} rows={6} required placeholder="Descreva o problema e o comportamento esperado..." />
      <p className="hint">Entre 10 e 2000 caracteres.</p>
      <label htmlFor="priority">Prioridade</label>
      <select id="priority" value={priority} onChange={e => setPriority(e.target.value as Priority)}>
        {(Object.keys(priorityLabels) as Priority[]).map(value => <option key={value} value={value}>{priorityLabels[value]}</option>)}
      </select>
      {error && <p role="alert" className="alert error">{error}</p>}
      <div className="form-actions"><button className="button primary" disabled={saving} type="submit">{saving ? 'Salvando...' : submitLabel}</button></div>
    </form>
  );
}
