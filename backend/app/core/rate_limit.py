"""Limitação de requisições em memória, por processo (ambiente local)."""
from collections import deque
from math import ceil
from threading import Lock
from time import monotonic

from fastapi import Depends, HTTPException, Request

from app.core.config import get_settings
from app.core.security import get_current_user
from app.models.user import User


class SlidingWindowLimiter:
    def __init__(self):
        self._lock = Lock()
        self._events: dict[str, deque[float]] = {}

    def clear(self):
        with self._lock:
            self._events.clear()

    def check(self, key: str, limit: int, window_seconds: int = 60):
        now = monotonic()
        with self._lock:
            # Remove entradas expiradas de todas as chaves para evitar crescimento ilimitado.
            for stored_key, timestamps in list(self._events.items()):
                while timestamps and now - timestamps[0] >= window_seconds:
                    timestamps.popleft()
                if not timestamps:
                    del self._events[stored_key]
            timestamps = self._events.setdefault(key, deque())
            if len(timestamps) >= limit:
                retry_after = max(1, ceil(window_seconds - (now - timestamps[0])))
                raise HTTPException(
                    status_code=429,
                    detail="Muitas requisições. Tente novamente mais tarde.",
                    headers={"Retry-After": str(retry_after)},
                )
            timestamps.append(now)


limiter = SlidingWindowLimiter()


def limit_login(request: Request):
    # Não confiar em X-Forwarded-For recebido diretamente do cliente.
    # Atrás de proxy, configurar corretamente os proxies confiáveis no servidor.
    ip = request.client.host if request.client else "unknown"
    limiter.check(f"login:{ip}", get_settings().login_rate_limit_per_minute)


def limit_ai(user: User = Depends(get_current_user)):
    limiter.check(f"ai:{user.id}", get_settings().ai_rate_limit_per_minute)
