"""Configuração isolada para os testes, sem depender do PostgreSQL local."""
import os
os.environ.setdefault("DATABASE_URL", "sqlite+pysqlite:///:memory:")
os.environ.setdefault("JWT_SECRET_KEY", "test-only-key-not-for-production-0123456789")
