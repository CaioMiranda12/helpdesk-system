import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { TicketForm } from './TicketForm';
import { aiTriageApi } from '../services/api';

vi.mock('../services/api', () => ({
  aiTriageApi: { suggest: vi.fn() },
  errorMessage: () => 'Falha na triagem.',
}));

beforeEach(() => vi.clearAllMocks());

async function fillForm(user: ReturnType<typeof userEvent.setup>) {
  await user.type(screen.getByLabelText(/título/i), 'Sistema fora do ar');
  await user.type(screen.getByLabelText(/descrição/i), 'Ninguém consegue emitir nota fiscal');
}

describe('TicketForm — triagem simulada', () => {
  it('exibe sugestão e só altera prioridade após confirmação', async () => {
    vi.mocked(aiTriageApi.suggest).mockResolvedValue({
      priority: 'high', category: 'software', reason: 'Impacto coletivo.', provider: 'mock',
    });
    const user = userEvent.setup();
    render(<TicketForm submitLabel="Criar chamado" onSubmit={vi.fn()} />);
    await fillForm(user);
    await user.click(screen.getByRole('button', { name: /sugerir com ia/i }));
    expect(await screen.findByText('Impacto coletivo.')).toBeInTheDocument();
    expect(screen.getByLabelText(/prioridade/i)).toHaveValue('medium');
    await user.click(screen.getByRole('button', { name: /aplicar prioridade sugerida/i }));
    expect(screen.getByLabelText(/prioridade/i)).toHaveValue('high');
  });

  it('não consulta API com texto insuficiente', async () => {
    const user = userEvent.setup();
    render(<TicketForm submitLabel="Criar chamado" onSubmit={vi.fn()} />);
    await user.click(screen.getByRole('button', { name: /sugerir com ia/i }));
    expect(screen.getByRole('alert')).toHaveTextContent('Preencha um título');
    expect(aiTriageApi.suggest).not.toHaveBeenCalled();
  });

  it('mostra falha e libera botão para tentar novamente', async () => {
    vi.mocked(aiTriageApi.suggest).mockRejectedValue(new Error('offline'));
    const user = userEvent.setup();
    render(<TicketForm submitLabel="Criar chamado" onSubmit={vi.fn()} />);
    await fillForm(user);
    await user.click(screen.getByRole('button', { name: /sugerir com ia/i }));
    expect(await screen.findByRole('alert')).toHaveTextContent('Falha na triagem.');
    await waitFor(() => expect(screen.getByRole('button', { name: /sugerir com ia/i })).toBeEnabled());
  });

  it('descarta sugestão se o texto do chamado for alterado', async () => {
    vi.mocked(aiTriageApi.suggest).mockResolvedValue({
      priority: 'high', category: 'software', reason: 'Impacto coletivo.', provider: 'mock',
    });
    const user = userEvent.setup();
    render(<TicketForm submitLabel="Criar chamado" onSubmit={vi.fn()} />);
    await fillForm(user);
    await user.click(screen.getByRole('button', { name: /sugerir com ia/i }));
    expect(await screen.findByText('Impacto coletivo.')).toBeInTheDocument();
    await user.type(screen.getByLabelText(/descrição/i), ' hoje');
    expect(screen.queryByText('Impacto coletivo.')).not.toBeInTheDocument();
  });
});
