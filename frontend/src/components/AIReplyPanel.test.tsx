import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { AIReplyPanel } from './AIReplyPanel';
import { aiReplyApi } from '../services/api';

vi.mock('../services/api', () => ({
  aiReplyApi: { suggest: vi.fn() },
  errorMessage: () => 'Falha ao gerar resposta.',
}));

beforeEach(() => vi.clearAllMocks());
const props = { title: 'Sistema fora do ar', description: 'Não consigo acessar o sistema desde ontem.' };

describe('AIReplyPanel', () => {
  it('gera um rascunho editável sem publicar automaticamente', async () => {
    vi.mocked(aiReplyApi.suggest).mockResolvedValue({ suggestion: 'Olá! Verifique o navegador.', provider: 'groq' });
    const user = userEvent.setup();
    render(<AIReplyPanel {...props} />);
    await user.click(screen.getByRole('button', { name: 'Sugerir resposta com IA' }));
    expect(await screen.findByLabelText('Rascunho editável')).toHaveValue('Olá! Verifique o navegador.');
    expect(screen.getByText('Provedor: groq')).toBeInTheDocument();
    expect(aiReplyApi.suggest).toHaveBeenCalledWith(props.title, props.description);
    const textarea = screen.getByLabelText('Rascunho editável');
    await user.clear(textarea);
    expect(textarea).toBeInTheDocument();
    await user.type(textarea, 'Resposta revisada');
    expect(screen.getByLabelText('Rascunho editável')).toHaveValue('Resposta revisada');
  });

  it('exibe falha e permite nova tentativa', async () => {
    vi.mocked(aiReplyApi.suggest).mockRejectedValue(new Error('offline'));
    const user = userEvent.setup();
    render(<AIReplyPanel {...props} />);
    await user.click(screen.getByRole('button', { name: 'Sugerir resposta com IA' }));
    expect(await screen.findByRole('alert')).toHaveTextContent('Falha ao gerar resposta.');
    await waitFor(() => expect(screen.getByRole('button', { name: 'Sugerir resposta com IA' })).toBeEnabled());
  });

  it('copia somente o texto revisado', async () => {
    vi.mocked(aiReplyApi.suggest).mockResolvedValue({ suggestion: 'Resposta inicial', provider: 'mock' });
    const user = userEvent.setup();
    const writeText = vi.fn().mockResolvedValue(undefined);
    Object.defineProperty(navigator, 'clipboard', { configurable: true, value: { writeText } });
    render(<AIReplyPanel {...props} />);
    await user.click(screen.getByRole('button', { name: 'Sugerir resposta com IA' }));
    await screen.findByLabelText('Rascunho editável');
    const textarea = screen.getByLabelText('Rascunho editável');
    await user.clear(textarea);
    expect(textarea).toBeInTheDocument();
    await user.type(textarea, 'Texto revisado');
    await user.click(screen.getByRole('button', { name: 'Copiar resposta' }));
    expect(writeText).toHaveBeenCalledWith('Texto revisado');
  });

  it('descarta rascunho ao trocar os dados do chamado', async () => {
    vi.mocked(aiReplyApi.suggest).mockResolvedValue({ suggestion: 'Resposta inicial', provider: 'mock' });
    const user = userEvent.setup();
    const { rerender } = render(<AIReplyPanel {...props} />);
    await user.click(screen.getByRole('button', { name: 'Sugerir resposta com IA' }));
    await screen.findByLabelText('Rascunho editável');
    rerender(<AIReplyPanel {...props} title="Outro chamado" />);
    expect(screen.queryByLabelText('Rascunho editável')).not.toBeInTheDocument();
  });
});
