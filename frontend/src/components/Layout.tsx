import { Link, NavLink, Outlet, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

export function Layout() {
  const { user, signOut } = useAuth();
  const navigate = useNavigate();
  function logout() { signOut(); navigate('/login', { replace: true }); }
  return <div className="app-shell">
    <header className="topbar"><div className="topbar-inner">
      <Link to="/" className="brand"><span className="brand-mark">H</span> Helpdesk <span className="brand-sub">/ Central de suporte</span></Link>
      <nav aria-label="Navegação principal"><NavLink to="/" end>Chamados</NavLink><NavLink to="/dashboard">Dashboard</NavLink><NavLink to="/tickets/new">Novo chamado</NavLink></nav>
      <div className="account"><span>{user?.name} ({user?.role === 'admin' ? 'Admin' : 'Agente'})</span><button className="button subtle" onClick={logout}>Sair</button></div>
    </div></header><main className="container"><Outlet /></main>
    <footer className="footer">Helpdesk System · Projeto de portfólio · Sprint 08</footer>
  </div>;
}
