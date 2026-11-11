from fastapi import FastAPI
from app.api.v1.tickets import router as tickets_router

app = FastAPI(
    title="Helpdesk API",
    description="API do Sistema de Gestão de Chamados",
    version="0.3.0",
)

@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}

app.include_router(tickets_router)
