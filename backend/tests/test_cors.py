from fastapi.testclient import TestClient

from app.config import Settings
from app.main import app


"""
CORS Tests

Browsers only let a web page call the API if the API allows the page's
origin. These tests send the same preflight request a browser sends
before a cross-origin call, and check the API's answer.
"""


client = TestClient(app)


def preflight(origin: str):
    """
    Send the OPTIONS request a browser makes before calling the API
    from a page at `origin`.
    """

    return client.options(
        "/health/status",
        headers={
            "Origin": origin,
            "Access-Control-Request-Method": "GET",
        },
    )


# Verify that the frontend's default origin is allowed.
def test_default_frontend_origin_is_allowed():

    response = preflight("http://localhost:5173")

    assert response.status_code == 200
    assert (
        response.headers["access-control-allow-origin"]
        == "http://localhost:5173"
    )


# Verify that any other origin is not allowed.
def test_other_origins_are_not_allowed():

    response = preflight("http://evil.example")

    assert "access-control-allow-origin" not in response.headers


# Verify that CORS_ALLOWED_ORIGINS defaults to the frontend's address.
def test_cors_allowed_origins_default():

    assert Settings.model_fields["CORS_ALLOWED_ORIGINS"].default == [
        "http://localhost:5173"
    ]


# Verify that CORS_ALLOWED_ORIGINS can be set as a JSON list.
def test_cors_allowed_origins_can_be_set(monkeypatch):

    monkeypatch.setenv(
        "CORS_ALLOWED_ORIGINS",
        '["http://localhost:5173", "http://127.0.0.1:5173"]',
    )

    assert Settings().CORS_ALLOWED_ORIGINS == [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]
