from pydantic_settings import BaseSettings


class Config(BaseSettings):
    database_url: str
    echo_sql: bool = True
    test: bool = False
    debug_logs: bool = False
    project_name: str = "Compress Links API"


CONFIG = Config()
