import { Link, useNavigate } from 'react-router-dom';
import { TicketForm } from '../components/TicketForm';
import { errorMessage, ticketsApi } from '../services/api';

export function TicketNew() {
  const navigate = useNavigate();
  return <><Link className="back-link" to="/">← Voltar aos chamados</Link><div className="page-heading"><div><p className="eyebrow">NOVA SOLICITAÇÃO</p><h1>Abrir chamado</h1><p className="muted">Descreva o problema para registrar uma solicitação.</p></div></div><TicketForm submitLabel="Criar chamado" onSubmit={async values => { try { const ticket = await ticketsApi.create(values); navigate(`/tickets/${ticket.id}`); } catch (err) { throw new Error(errorMessage(err)); } }} /></>;
}
