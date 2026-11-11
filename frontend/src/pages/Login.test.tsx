import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import { describe, expect, it, vi } from 'vitest';
import { Login } from './Login';

const signIn = vi.fn();
vi.mock('../contexts/AuthContext', () => ({
  useAuth: () => ({ user: null, signIn }),
}));

describe('Login', () => {
  it('envia credenciais e navega após autenticação', async () => {
    signIn.mockResolvedValueOnce(undefined);
    const user = userEvent.setup();
    render(<MemoryRouter initialEntries={['/login']}><Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/" element={<h1>Área interna</h1>} />
    </Routes></MemoryRouter>);
    await user.type(screen.getByLabelText(/e-mail/i), 'agente@example.com');
    await user.type(screen.getByLabelText(/senha/i), 'minha-senha-de-teste');
    await user.click(screen.getByRole('button', { name: 'Entrar' }));
    expect(await screen.findByRole('heading', { name: 'Área interna' })).toBeInTheDocument();
    expect(signIn).toHaveBeenCalledWith('agente@example.com', 'minha-senha-de-teste');
  });
  it('mostra mensagem quando o login falha', async () => {
    signIn.mockRejectedValueOnce(new Error('Credenciais inválidas'));
    const user = userEvent.setup();
    render(<MemoryRouter><Login /></MemoryRouter>);
    await user.type(screen.getByLabelText(/e-mail/i), 'agente@example.com');
    await user.type(screen.getByLabelText(/senha/i), 'senha-incorreta');
    await user.click(screen.getByRole('button', { name: 'Entrar' }));
    expect(await screen.findByRole('alert')).toHaveTextContent(/E-mail ou senha inválidos/);
  });
});
