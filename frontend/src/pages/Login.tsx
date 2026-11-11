import { useState } from 'react';
import { Navigate, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

export function Login() {
  const { user, signIn } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();
  if (user) return <Navigate to="/" replace />;
  async function submit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault(); setError(''); setSubmitting(true);
    try {
      await signIn(email, password);
      const from = (location.state as { from?: string } | null)?.from;
      navigate(from && from.startsWith('/') && !from.startsWith('//') ? from : '/', { replace: true });
    } catch { setError('E-mail ou senha inválidos, ou a API está indisponível.'); }
    finally { setSubmitting(false); }
  }
  return <div className="login-screen"><form className="card login-card" onSubmit={submit}>
    <div className="brand"><span className="brand-mark">H</span> Helpdesk</div>
    <h1>Entrar no sistema</h1><p className="muted">Acesse com sua conta de administrador ou agente.</p>
    {error && <p className="alert error" role="alert">{error}</p>}
    <label htmlFor="login-email">E-mail</label><input id="login-email" type="email" autoComplete="username" required value={email} onChange={e => setEmail(e.target.value)} />
    <label htmlFor="login-password">Senha</label><input id="login-password" type="password" autoComplete="current-password" required value={password} onChange={e => setPassword(e.target.value)} />
    <button className="button primary" disabled={submitting}>{submitting ? 'Entrando...' : 'Entrar'}</button>
  </form></div>;
}
