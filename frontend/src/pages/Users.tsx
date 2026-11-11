import { useEffect, useState } from 'react';
import axios from 'axios';
import type { FormEvent } from 'react';
import type { CurrentUser } from '../services/auth';
import { usersApi } from '../services/users';
import type { CreateUser } from '../services/users';

const initial: CreateUser = { name: '', email: '', password: '', role: 'agent' };

function message(error: unknown): string {
  if (axios.isAxiosError(error)) {
    if (!error.response) return 'Não foi possível conectar à API.';
    if (error.response.status === 409) return 'Este e-mail já está cadastrado.';
    if (error.response.status === 403) return 'Somente administradores podem gerenciar usuários.';
    if (error.response.status === 422) return 'Confira os dados. A senha deve ter pelo menos 12 caracteres.';
  }
  return 'Não foi possível concluir a operação.';
}

export function Users() {
  const [users, setUsers] = useState<CurrentUser[]>([]);
  const [form, setForm] = useState<CreateUser>(initial);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  async function refresh() {
    setLoading(true); setError('');
    try { setUsers(await usersApi.list()); }
    catch (err) { setError(message(err)); }
    finally { setLoading(false); }
  }
  useEffect(() => { void refresh(); }, []);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault(); setError(''); setSuccess(''); setSaving(true);
    try {
      await usersApi.create({ ...form, name: form.name.trim(), email: form.email.trim().toLowerCase() });
      setForm(initial); setSuccess('Usuário cadastrado com sucesso.');
      await refresh();
    } catch (err) { setError(message(err)); }
    finally { setSaving(false); }
  }

  return <section>
    <div className="page-heading"><div><p className="eyebrow">ADMINISTRAÇÃO</p><h1>Usuários</h1><p className="muted">Cadastre e consulte os usuários da central de suporte.</p></div></div>
    <div className="users-grid">
      <form className="card form users-form" onSubmit={submit}>
        <h2>Novo usuário</h2>
        <label htmlFor="user-name">Nome</label>
        <input id="user-name" required minLength={2} maxLength={120} value={form.name} onChange={e => setForm({ ...form, name: e.target.value })} />
        <label htmlFor="user-email">E-mail</label>
        <input id="user-email" required type="email" value={form.email} onChange={e => setForm({ ...form, email: e.target.value })} />
        <label htmlFor="user-password">Senha inicial</label>
        <input id="user-password" required type="password" minLength={12} maxLength={128} autoComplete="new-password" value={form.password} onChange={e => setForm({ ...form, password: e.target.value })} />
        <p className="hint">Mínimo de 12 caracteres. Compartilhe a senha por um canal seguro.</p>
        <label htmlFor="user-role">Perfil</label>
        <select id="user-role" value={form.role} onChange={e => setForm({ ...form, role: e.target.value as CreateUser['role'] })}>
          <option value="agent">Agente</option><option value="admin">Administrador</option>
        </select>
        <div className="form-actions"><button className="button primary" disabled={saving}>{saving ? 'Salvando...' : 'Cadastrar usuário'}</button></div>
        {success && <p className="alert success" role="status">{success}</p>}
      </form>
      <div className="card table-card users-table">
        <div className="users-table-heading"><h2>Usuários cadastrados</h2><button type="button" className="button subtle" onClick={() => void refresh()} disabled={loading}>Atualizar</button></div>
        {error && <p className="alert error" role="alert">{error}</p>}
        {loading ? <p className="state-message">Carregando usuários...</p> : users.length === 0 ? <p className="state-message">Nenhum usuário encontrado.</p> : <div className="table-scroll"><table><thead><tr><th>Nome</th><th>E-mail</th><th>Perfil</th></tr></thead><tbody>
          {users.map(user => <tr key={user.id}><td>{user.name}</td><td>{user.email}</td><td><span className="pill status-open">{user.role === 'admin' ? 'Administrador' : 'Agente'}</span></td></tr>)}
        </tbody></table></div>}
        <p className="hint users-note">Exibindo até 100 usuários. Paginação completa ficará para uma próxima melhoria.</p>
      </div>
    </div>
  </section>;
}
