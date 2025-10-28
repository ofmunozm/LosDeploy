import json
from types import SimpleNamespace
from unittest.mock import MagicMock
import pytest

def token_header(mod):
    token = getattr(mod, "Config", None)
    if token is None:
        return {}
    return {"Authorization": f"Bearer {mod.Config.STATIC_TOKEN}"}


def test_health_check(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "unhealthy"} # Esto debería ser "healthy, se modifica para prueba"


def test_token_required_missing(client):
    resp = client.post("/blacklists", json={})
    assert resp.status_code == 401
    data = resp.get_json()
    assert "error" in data


def test_token_required_invalid(client, mod):
    headers = {"Authorization": "Bearer invalid-token"}
    resp = client.post("/blacklists", json={}, headers=headers)
    assert resp.status_code == 401
    data = resp.get_json()
    assert "error" in data


def test_add_to_blacklist_missing_fields(client, mod):
    headers = token_header(mod)
    resp = client.post("/blacklists", json=None, headers=headers)
    assert resp.status_code == 400
    data = resp.get_json()
    assert "error" in data


def test_add_to_blacklist_blocked_reason_too_long(client, mod, monkeypatch):
    headers = token_header(mod)
    long_reason = "x" * 256
    session = MagicMock()
    db_mock = MagicMock()
    db_mock.session = session
    monkeypatch.setattr(mod, "db", db_mock)

    blacklist_mock = MagicMock()
    q = MagicMock()
    q.filter_by.return_value.first.return_value = None
    blacklist_mock.query = q
    monkeypatch.setattr(mod, "Blacklist", blacklist_mock)

    payload = {"email": "a@b.com", "app_uuid": "uuid", "blocked_reason": long_reason}
    resp = client.post("/blacklists", json=payload, headers=headers)
    assert resp.status_code == 400
    assert "blocked_reason" in resp.get_json().get("error", "") or "blocked_reason" in resp.get_json().get("error", "")


def test_add_to_blacklist_existing_email(client, mod, monkeypatch):
    headers = token_header(mod)
    existing_obj = SimpleNamespace(email="a@b.com", blocked_reason="motivo")
    q = MagicMock()
    q.filter_by.return_value.first.return_value = existing_obj

    blacklist_mock = MagicMock()
    blacklist_mock.query = q
    monkeypatch.setattr(mod, "Blacklist", blacklist_mock)

    session = MagicMock()
    db_mock = MagicMock()
    db_mock.session = session
    monkeypatch.setattr(mod, "db", db_mock)

    payload = {"email": "a@b.com", "app_uuid": "uuid"}
    resp = client.post("/blacklists", json=payload, headers=headers)
    assert resp.status_code == 200
    data = resp.get_json()
    assert data.get("message") == "El email ya está en la lista negra"
    assert not db_mock.session.add.called
    assert not db_mock.session.commit.called


def test_add_to_blacklist_success(client, mod, monkeypatch):
    headers = token_header(mod)

    q = MagicMock()
    q.filter_by.return_value.first.return_value = None

    blacklist_mock = MagicMock()
    blacklist_mock.query = q
    monkeypatch.setattr(mod, "Blacklist", blacklist_mock)

    session = MagicMock()
    db_mock = MagicMock()
    db_mock.session = session
    monkeypatch.setattr(mod, "db", db_mock)

    payload = {"email": "nuevo@ejemplo.com", "app_uuid": "uuid", "blocked_reason": "ok"}
    resp = client.post("/blacklists", json=payload, headers=headers)
    assert resp.status_code == 201
    data = resp.get_json()
    assert "agregado" in data.get("message", "").lower() or "exitosamente" in data.get("message", "").lower()
    assert db_mock.session.add.called
    assert db_mock.session.commit.called


def test_check_blacklist_in(client, mod, monkeypatch):
    headers = token_header(mod)

    existing_obj = SimpleNamespace(email="a@b.com", blocked_reason="spam")
    q = MagicMock()
    q.filter_by.return_value.first.return_value = existing_obj

    blacklist_mock = MagicMock()
    blacklist_mock.query = q
    monkeypatch.setattr(mod, "Blacklist", blacklist_mock)

    resp = client.get("/blacklists/a@b.com", headers=headers)
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["in_blacklist"] is True
    assert data["blocked_reason"] == "spam"


def test_check_blacklist_not_in(client, mod, monkeypatch):
    headers = token_header(mod)

    q = MagicMock()
    q.filter_by.return_value.first.return_value = None

    blacklist_mock = MagicMock()
    blacklist_mock.query = q
    monkeypatch.setattr(mod, "Blacklist", blacklist_mock)

    resp = client.get("/blacklists/noexiste@ejemplo.com", headers=headers)
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["in_blacklist"] is False