import { BrowserRouter, Navigate, Outlet, Route, Routes, useLocation } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import { Layout } from './components/Layout';
import { TicketDetail } from './pages/TicketDetail';
import { TicketList } from './pages/TicketList';
import { TicketNew } from './pages/TicketNew';
import { Dashboard } from './pages/Dashboard';
import { Login } from './pages/Login';
import { Users } from './pages/Users';

function AdminOnly() {
  const { user } = useAuth();
  return user?.role === 'admin' ? <Outlet /> : <Navigate to="/" replace />;
}
function Protected() {
  const { user, loading } = useAuth();
  const location = useLocation();
  if (loading) return <p className="state-message">Verificando sessão...</p>;
  if (!user) return <Navigate to="/login" state={{ from: location.pathname }} replace />;
  return <Outlet />;
}
export default function App() {
  return <BrowserRouter><AuthProvider><Routes>
    <Route path="/login" element={<Login />} />
    <Route element={<Protected />}><Route element={<Layout />}>
      <Route path="/" element={<TicketList />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route element={<AdminOnly />}><Route path="/users" element={<Users />} /></Route>
      <Route path="/tickets/new" element={<TicketNew />} />
      <Route path="/tickets/:id" element={<TicketDetail />} />
      <Route path="*" element={<div className="card state-message"><h1>Página não encontrada</h1></div>} />
    </Route></Route>
  </Routes></AuthProvider></BrowserRouter>;
}
