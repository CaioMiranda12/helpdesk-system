from test_ticket_api import client, PAYLOAD


def add(client, title, priority="medium", status="open"):
    created = client.post("/api/v1/tickets", json={**PAYLOAD, "title": title, "priority": priority})
    assert created.status_code == 201
    ticket_id = created.json()["id"]
    if status in ("in_progress", "resolved"):
        assert client.patch(f"/api/v1/tickets/{ticket_id}/status", json={"status": "in_progress"}).status_code == 200
    if status == "resolved":
        assert client.patch(f"/api/v1/tickets/{ticket_id}/status", json={"status": "resolved"}).status_code == 200
    return ticket_id


def test_empty_dashboard(client):
    response = client.get("/api/v1/dashboard/summary")
    assert response.status_code == 200
    assert response.json() == {
        "total": 0,
        "by_status": {"open": 0, "in_progress": 0, "resolved": 0},
        "by_priority": {"low": 0, "medium": 0, "high": 0},
    }


def test_dashboard_aggregates_all_tickets(client):
    add(client, "Falha de impressão", "low", "open")
    add(client, "Erro de autenticação", "high", "in_progress")
    add(client, "Relatório indisponível", "high", "resolved")
    add(client, "Problema de conexão", "medium", "open")
    response = client.get("/api/v1/dashboard/summary")
    assert response.status_code == 200
    assert response.json() == {
        "total": 4,
        "by_status": {"open": 2, "in_progress": 1, "resolved": 1},
        "by_priority": {"low": 1, "medium": 1, "high": 2},
    }


def test_dashboard_updates_after_status_change(client):
    ticket_id = add(client, "Servidor indisponível", "high")
    before = client.get("/api/v1/dashboard/summary").json()
    assert before["by_status"]["open"] == 1
    client.patch(f"/api/v1/tickets/{ticket_id}/status", json={"status": "in_progress"})
    after = client.get("/api/v1/dashboard/summary").json()
    assert after["by_status"] == {"open": 0, "in_progress": 1, "resolved": 0}
    assert after["total"] == 1


def test_dashboard_is_not_limited_by_ticket_pagination(client):
    for i in range(23):
        add(client, f"Chamado de teste {i}", "medium")
    assert len(client.get("/api/v1/tickets", params={"limit": 10}).json()) == 10
    assert client.get("/api/v1/dashboard/summary").json()["total"] == 23
