"""Tests for Configuration."""

from backend.core.config import Settings, settings


class TestSettings:
    def test_default_values(self):
        s = Settings()
        assert s.APP_NAME == "Nova AI"
        assert s.APP_VERSION == "1.0.0"
        assert s.DEBUG is True
        assert s.PORT == 8000

    def test_is_production(self):
        dev = Settings(APP_ENV="development")
        prod = Settings(APP_ENV="production")
        assert dev.is_production is False
        assert prod.is_production is True

    def test_database_url_default(self):
        s = Settings()
        assert "sqlite" in s.database_url
        assert s.database_url == s.DATABASE_URL

    def test_database_url_postgres(self):
        s = Settings(POSTGRES_URL="postgresql://user:pass@localhost/db")
        assert "postgresql" in s.database_url
        assert s.database_url != s.DATABASE_URL

    def test_singleton(self):
        from backend.core.config import get_settings
        s1 = get_settings()
        s2 = get_settings()
        assert s1 is s2


def test_settings_instance():
    assert settings.APP_NAME == "Nova AI"
    assert hasattr(settings, "SECRET_KEY")
    assert hasattr(settings, "OPENAI_API_KEY")
