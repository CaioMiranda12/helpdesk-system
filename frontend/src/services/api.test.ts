import { AxiosError } from 'axios';
import { describe, expect, it } from 'vitest';
import { errorMessage } from './api';

describe('errorMessage', () => {
  it('distingue falha de conexão', () => {
    expect(errorMessage(new AxiosError('Network Error', 'ERR_NETWORK'))).toMatch(/conectar à API/);
  });
  it('distingue timeout', () => {
    expect(errorMessage(new AxiosError('timeout', 'ECONNABORTED'))).toMatch(/demorou para responder/);
  });
  it('informa ausência de permissão para HTTP 403', () => {
    const error = new AxiosError('Forbidden', 'ERR_BAD_RESPONSE', undefined, undefined, {
      data: {}, status: 403, statusText: 'Forbidden', headers: {}, config: { headers: {} as never },
    });
    expect(errorMessage(error)).toMatch(/não tem permissão/);
  });
});
