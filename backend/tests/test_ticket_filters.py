from test_ticket_api import client  # fixture compartilhada da Sprint 03
from test_ticket_api import PAYLOAD

def seed(client, title, priority="medium", status="open"):
    ticket = client.post("/api/v1/tickets", json={**PAYLOAD, "title": title, "priority": priority}).json()
    if status != "open":
        client.patch(f"/api/v1/tickets/{ticket['id']}/status", json={"status": "in_progress"})
    if status == "resolved":
        client.patch(f"/api/v1/tickets/{ticket['id']}/status", json={"status": "resolved"})
    return ticket

def test_search_is_case_insensitive(client):
    seed(client, "Falha no RELATORIO")
    seed(client, "Problema no login")
    response = client.get("/api/v1/tickets", params={"search": "relatorio"})
    assert response.status_code == 200
    assert [item["title"] for item in response.json()] == ["Falha no RELATORIO"]

def test_filters_can_be_combined(client):
    expected = seed(client, "Relatório mensal", "high", "in_progress")
    seed(client, "Relatório semanal", "low", "in_progress")
    seed(client, "Relatório anual", "high", "open")
    seed(client, "Erro no login", "high", "in_progress")
    response = client.get("/api/v1/tickets", params={"search": "relatório", "status": "in_progress", "priority": "high"})
    assert response.status_code == 200
    assert [item["id"] for item in response.json()] == [expected["id"]]

def test_pagination_applies_after_filtering(client):
    for i in range(5): seed(client, f"Relatório {i} do setor", "high")
    for i in range(3): seed(client, f"Outro chamado {i}", "low")
    first = client.get("/api/v1/tickets", params={"priority": "high", "limit": 3, "offset": 0})
    second = client.get("/api/v1/tickets", params={"priority": "high", "limit": 3, "offset": 3})
    assert len(first.json()) == 3
    assert len(second.json()) == 2
    assert not ({t["id"] for t in first.json()} & {t["id"] for t in second.json()})

def test_invalid_filter_values_are_rejected(client):
    assert client.get("/api/v1/tickets?status=invalid").status_code == 422
    assert client.get("/api/v1/tickets?priority=urgent").status_code == 422
    assert client.get("/api/v1/tickets", params={"search": "x" * 121}).status_code == 422

def test_search_treats_sql_wildcards_as_literals(client):
    seed(client, "Relatório 100% pronto")
    seed(client, "Relatório 1000 pronto")
    response = client.get("/api/v1/tickets", params={"search": "%"})
    assert [t["title"] for t in response.json()] == ["Relatório 100% pronto"]
    assert client.get("/api/v1/tickets", params={"search": "_"}).json() == []
