import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it, vi } from 'vitest';
import { TicketForm } from './TicketForm';

describe('TicketForm', () => {
  it('envia os campos preenchidos e remove espaços nas extremidades', async () => {
    const onSubmit = vi.fn().mockResolvedValue(undefined);
    const user = userEvent.setup();
    render(<TicketForm submitLabel="Criar chamado" onSubmit={onSubmit} />);
    await user.type(screen.getByLabelText(/título/i), '  Impressora sem papel  ');
    await user.type(screen.getByLabelText(/descrição/i), '  Não consigo imprimir documentos  ');
    await user.selectOptions(screen.getByLabelText(/prioridade/i), 'high');
    await user.click(screen.getByRole('button', { name: 'Criar chamado' }));
    await waitFor(() => expect(onSubmit).toHaveBeenCalledWith({
      title: 'Impressora sem papel',
      description: 'Não consigo imprimir documentos',
      priority: 'high',
    }));
  });

  it('impede envio quando o título não alcança o tamanho mínimo', async () => {
    const onSubmit = vi.fn();
    const user = userEvent.setup();
    render(<TicketForm submitLabel="Salvar" onSubmit={onSubmit} />);
    await user.type(screen.getByLabelText(/título/i), 'ABC');
    await user.type(screen.getByLabelText(/descrição/i), 'Descrição suficientemente longa');
    await user.click(screen.getByRole('button', { name: 'Salvar' }));
    expect(onSubmit).not.toHaveBeenCalled();
    expect(screen.getByLabelText(/título/i)).toHaveAttribute(
      'minLength',
      '5'
    );
  });

  it('mostra erro e libera botão se a gravação falhar', async () => {
    const onSubmit = vi.fn().mockRejectedValue(new Error('Falha ao salvar chamado'));
    const user = userEvent.setup();
    render(<TicketForm submitLabel="Salvar" onSubmit={onSubmit} />);
    await user.type(screen.getByLabelText(/título/i), 'Impressora sem papel');
    await user.type(screen.getByLabelText(/descrição/i), 'Descrição suficientemente longa');
    await user.click(screen.getByRole('button', { name: 'Salvar' }));
    expect(await screen.findByRole('alert')).toHaveTextContent('Falha ao salvar chamado');
    expect(screen.getByRole('button', { name: 'Salvar' })).toBeEnabled();
  });
});
