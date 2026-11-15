import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { AIActivitySummaryPanel } from './AIActivitySummaryPanel';
import { aiActivitySummaryApi } from '../services/activities';

vi.mock('../services/activities', () => ({ aiActivitySummaryApi: { summarize: vi.fn() } }));
vi.mock('../services/api', () => ({ errorMessage: () => 'Não foi possível gerar o resumo.' }));

const props = { ticketId: 'ticket-1', refreshKey: 0, hasActivities: true };
beforeEach(() => vi.clearAllMocks());

describe('AIActivitySummaryPanel', () => {
  it('gera e exibe resumo somente após clique', async () => {
    vi.mocked(aiActivitySummaryApi.summarize).mockResolvedValue({
      summary: 'Chamado em atendimento, aguardando retorno.', provider: 'groq', activities_considered: 3,
    });
    const user = userEvent.setup();
    render(<AIActivitySummaryPanel {...props} />);
    expect(aiActivitySummaryApi.summarize).not.toHaveBeenCalled();
    await user.click(screen.getByRole('button', { name: 'Resumir atividades com IA' }));
    expect(await screen.findByText('Chamado em atendimento, aguardando retorno.')).toBeInTheDocument();
    expect(screen.getByText(/Provedor: groq/)).toBeInTheDocument();
    expect(aiActivitySummaryApi.summarize).toHaveBeenCalledWith('ticket-1');
  });

  it('não permite gerar quando não existem atividades', () => {
    render(<AIActivitySummaryPanel {...props} hasActivities={false} />);
    expect(screen.getByRole('button', { name: 'Resumir atividades com IA' })).toBeDisabled();
  });

  it('exibe falha e permite tentar novamente', async () => {
    vi.mocked(aiActivitySummaryApi.summarize).mockRejectedValue(new Error('offline'));
    const user = userEvent.setup();
    render(<AIActivitySummaryPanel {...props} />);
    await user.click(screen.getByRole('button', { name: 'Resumir atividades com IA' }));
    expect(await screen.findByRole('alert')).toHaveTextContent('Não foi possível gerar o resumo.');
    await waitFor(() => expect(screen.getByRole('button', { name: 'Resumir atividades com IA' })).toBeEnabled());
  });

  it('descarta o resumo ao atualizar o histórico', async () => {
    vi.mocked(aiActivitySummaryApi.summarize).mockResolvedValue({
      summary: 'Resumo anterior de atividades.', provider: 'mock', activities_considered: 1,
    });
    const user = userEvent.setup();
    const { rerender } = render(<AIActivitySummaryPanel {...props} />);
    await user.click(screen.getByRole('button', { name: 'Resumir atividades com IA' }));
    await screen.findByText('Resumo anterior de atividades.');
    rerender(<AIActivitySummaryPanel {...props} refreshKey={1} />);
    await waitFor(() => expect(screen.queryByText('Resumo anterior de atividades.')).not.toBeInTheDocument());
  });
});
