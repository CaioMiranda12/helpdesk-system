"""Paginação do histórico: limites, isolamento e ordenação."""
from test_activities import scenario, new_ticket


def test_pages_do_not_repeat_and_follow_descending_order(scenario):
    client, _, _ = scenario
    ticket_id = new_ticket(client)
    for i in range(25):
        assert client.post(f"/api/v1/tickets/{ticket_id}/comments", json={"body": f"Comentário {i}"}).status_code == 201
    url = f"/api/v1/tickets/{ticket_id}/activities"
    first = client.get(url, params={"limit": 11, "offset": 0})
    second = client.get(url, params={"limit": 11, "offset": 10})
    last = client.get(url, params={"limit": 11, "offset": 20})
    assert first.status_code == second.status_code == last.status_code == 200
    assert len(first.json()) == len(second.json()) == 11
    assert len(last.json()) == 5
    ids_first = {item["id"] for item in first.json()[:10]}
    ids_second = {item["id"] for item in second.json()[:10]}
    ids_last = {item["id"] for item in last.json()}
    assert not (ids_first & ids_second or ids_first & ids_last or ids_second & ids_last)
    all_events = first.json()[:10] + second.json()[:10] + last.json()
    assert len(all_events) == 25
    assert [(event["created_at"], event["id"]) for event in all_events] == sorted(
        [(event["created_at"], event["id"]) for event in all_events], reverse=True
    )


def test_activity_list_is_scoped_to_ticket(scenario):
    client, _, _ = scenario
    first = new_ticket(client)
    second = new_ticket(client)
    for tid, body in ((first, "Primeiro chamado"), (second, "Segundo chamado")):
        assert client.post(f"/api/v1/tickets/{tid}/comments", json={"body": body}).status_code == 201
    response = client.get(f"/api/v1/tickets/{first}/activities")
    assert response.status_code == 200
    assert [event["body"] for event in response.json()] == ["Primeiro chamado"]


def test_pagination_boundaries(scenario):
    client, _, _ = scenario
    ticket_id = new_ticket(client)
    url = f"/api/v1/tickets/{ticket_id}/activities"
    assert client.get(url, params={"limit": 0}).status_code == 422
    assert client.get(url, params={"offset": -1}).status_code == 422
    assert client.get(url, params={"limit": 101}).status_code == 422
    assert client.get(url, params={"offset": 500}).json() == []


def test_activity_response_does_not_expose_password_hash(scenario):
    client, _, _ = scenario
    ticket_id = new_ticket(client)
    client.post(f"/api/v1/tickets/{ticket_id}/comments", json={"body": "Teste de privacidade"})
    response = client.get(f"/api/v1/tickets/{ticket_id}/activities")
    assert response.status_code == 200
    assert "password_hash" not in str(response.json())
