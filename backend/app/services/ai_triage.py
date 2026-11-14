"""Triagem simulada, determinística e sem serviços externos.

Não representa um modelo de IA generativa; serve para validar a integração.
"""
import re
import unicodedata
from app.schemas.ai_triage import AITriageRequest, AITriageResponse, TriageCategory
from app.schemas.ticket import Priority


def _normalize(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value.casefold())
    return "".join(char for char in normalized if not unicodedata.combining(char))


def _matches(text: str, words: tuple[str, ...]) -> bool:
    return any(re.search(r"(?<!\w)" + re.escape(word) + r"(?!\w)", text) for word in words)


def suggest_triage(payload: AITriageRequest) -> AITriageResponse:
    text = _normalize(f"{payload.title} {payload.description}")
    if _matches(text, ("senha", "login", "acesso", "bloqueado", "permissao", "autenticacao")):
        category = TriageCategory.access
    elif _matches(text, ("rede", "internet", "wifi", "servidor", "vpn", "conexao")):
        category = TriageCategory.infrastructure
    elif _matches(text, ("sistema", "aplicativo", "software", "erro", "bug", "nota fiscal")):
        category = TriageCategory.software
    elif _matches(text, ("computador", "notebook", "monitor", "impressora", "teclado")):
        category = TriageCategory.hardware
    else:
        category = TriageCategory.general

    if _matches(text, ("fora do ar", "parado", "indisponivel", "urgente", "critico", "ninguem consegue", "todos os usuarios")):
        priority = Priority.high
        reason = "Possível indisponibilidade ou impacto coletivo identificado no texto."
    elif _matches(text, ("nao funciona", "falha", "erro", "bloqueado", "sem acesso", "lento")):
        priority = Priority.medium
        reason = "Possível falha operacional identificada no texto."
    else:
        priority = Priority.low
        reason = "Não foram encontrados indicadores explícitos de urgência."

    return AITriageResponse(priority=priority, category=category, reason=reason)
