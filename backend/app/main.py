from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.tickets import router as tickets_router
from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.auth import router as auth_router

app = FastAPI(title="Helpdesk API", description="API do Sistema de Gestão de Chamados", version="0.8.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PATCH"],
    allow_headers=["Content-Type", "Authorization"],
)

@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}

app.include_router(auth_router)
app.include_router(tickets_router)
app.include_router(dashboard_router)
