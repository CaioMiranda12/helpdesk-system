"""Minimização conservadora de dados em textos enviados a provedores externos.

Não garante anonimização: revise conteúdo livre antes de enviá-lo a terceiros.
"""
import re

_PATTERNS = (
    (re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/-]+=*"), "[TOKEN_REMOVIDO]"),
    (re.compile(r"(?i)\b(?:sk-[A-Za-z0-9_-]{12,}|gsk_[A-Za-z0-9_-]{12,})\b"), "[CHAVE_REMOVIDA]"),
    (re.compile(r"(?<![\w.+-])[\w.+-]+@(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,}(?![\w-])"), "[EMAIL_REMOVIDO]"),
    (re.compile(r"(?<!\d)\d{3}\.\d{3}\.\d{3}-\d{2}(?!\d)"), "[CPF_REMOVIDO]"),
    (re.compile(r"(?<!\d)(?:\+55[\s.-]?)?\(?\d{2}\)?[\s.-]?9?\d{4}[\s.-]?\d{4}(?!\d)"), "[TELEFONE_REMOVIDO]"),
)


def minimize_for_external_ai(text: str) -> str:
    """Substitui padrões reconhecíveis sem alterar os dados persistidos."""
    for pattern, replacement in _PATTERNS:
        text = pattern.sub(replacement, text)
    return text
