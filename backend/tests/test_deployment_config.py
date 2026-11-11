from app.core.config import Settings


def test_cors_origins_are_parsed_and_normalized():
    settings = Settings(database_url="sqlite://", jwt_secret_key="test-secret", cors_origins=" https://example.com/ , http://localhost:5173, ")
    assert settings.allowed_origins == ["https://example.com", "http://localhost:5173"]


def test_cors_origins_do_not_allow_wildcard_by_default():
    settings = Settings(database_url="sqlite://", jwt_secret_key="test-secret")
    assert "*" not in settings.allowed_origins
