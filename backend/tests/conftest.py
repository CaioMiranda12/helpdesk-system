"""URL isolada para importação da aplicação em testes sem PostgreSQL local."""
import os
os.environ.setdefault("DATABASE_URL", "sqlite+pysqlite:///:memory:")
