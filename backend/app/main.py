from fastapi import FastAPI
from app.core.config import get_settings
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.tickets import router as tickets_router
from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.auth import router as auth_router
from app.api.v1.agents import router as agents_router

from app.api.v1.activities import router as activities_router

settings = get_settings()
if settings.app_environment == "production" and (len(settings.jwt_secret_key) < 32 or settings.jwt_secret_key.startswith("substitua-")):
    raise RuntimeError("JWT_SECRET_KEY deve ser uma chave forte em produção")

app = FastAPI(title="Helpdesk API", description="API do Sistema de Gestão de Chamados", version="0.14.0", docs_url=None if settings.app_environment == "production" else "/docs", redoc_url=None if settings.app_environment == "production" else "/redoc")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "PATCH"],
    allow_headers=["Content-Type", "Authorization"],
)

@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}

app.include_router(auth_router)
app.include_router(agents_router)
app.include_router(tickets_router)
app.include_router(activities_router)
app.include_router(dashboard_router)
