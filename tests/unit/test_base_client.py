from unittest.mock import Mock

from clients.base_client import BaseClient
from config.settings import REQUEST_TIMEOUT


def test_base_client_builds_url_and_applies_default_timeout(monkeypatch):
    client = BaseClient(token="abc")
    mocked_response = Mock(status_code=200)
    request = Mock(return_value=mocked_response)
    monkeypatch.setattr(client.session, "request", request)

    response = client.get("/articles", params={"limit": 5})

    assert response is mocked_response
    request.assert_called_once_with(
        method="GET",
        url=f"{client.base_url}/articles",
        params={"limit": 5},
        timeout=REQUEST_TIMEOUT,
    )
    assert client.session.headers["Authorization"] == "Token abc"
    client.close()


def test_explicit_timeout_overrides_default(monkeypatch):
    client = BaseClient()
    request = Mock(return_value=Mock(status_code=200))
    monkeypatch.setattr(client.session, "request", request)

    client.post("/users", json={"user": {}}, timeout=2)

    request.assert_called_once_with(
        method="POST",
        url=f"{client.base_url}/users",
        json={"user": {}},
        timeout=2,
    )
    client.close()


def test_clear_token_removes_authorization_header():
    client = BaseClient(token="abc")
    client.clear_token()
    assert "Authorization" not in client.session.headers
    client.close()
