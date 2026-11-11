
from fastapi import FastAPI

app = FastAPI(
    title="Helpdesk API",
    description="API do Sistema de Gestão de Chamados",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok"}
