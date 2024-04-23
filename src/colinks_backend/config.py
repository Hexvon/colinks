from pydantic_settings import BaseSettings


class Config(BaseSettings):
    database_url: str


CONFIG = Config()
