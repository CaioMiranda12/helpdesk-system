import { Link, NavLink, Outlet } from 'react-router-dom';

export function Layout() {
  return (
    <div className="app-shell">
      <header className="topbar">
        <div className="topbar-inner">
          <Link to="/" className="brand"><span className="brand-mark">H</span> Helpdesk <span className="brand-sub">/ Central de suporte</span></Link>
          <nav aria-label="Navegação principal">
            <NavLink to="/" end>Chamados</NavLink>
            <NavLink to="/dashboard">Dashboard</NavLink>
            <NavLink to="/tickets/new">Novo chamado</NavLink>
          </nav>
        </div>
      </header>
      <main className="container"><Outlet /></main>
      <footer className="footer">Helpdesk System · Projeto de portfólio · MVP sem autenticação</footer>
    </div>
  );
}
