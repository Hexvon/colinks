from colinks_backend.config import Config


class TestConfig(Config):
    test_database_url: str


TEST_CONFIG = TestConfig()
