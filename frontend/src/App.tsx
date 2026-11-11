import { BrowserRouter, Route, Routes } from 'react-router-dom';
import { Layout } from './components/Layout';
import { TicketDetail } from './pages/TicketDetail';
import { TicketList } from './pages/TicketList';
import { TicketNew } from './pages/TicketNew';
import { Dashboard } from './pages/Dashboard';

export default function App() {
  return <BrowserRouter><Routes><Route element={<Layout />}><Route path="/" element={<TicketList />} /><Route path="/dashboard" element={<Dashboard />} /><Route path="/tickets/new" element={<TicketNew />} /><Route path="/tickets/:id" element={<TicketDetail />} /><Route path="*" element={<div className="card state-message"><h1>Página não encontrada</h1><a href="/">Voltar ao início</a></div>} /></Route></Routes></BrowserRouter>;
}
