from pydantic_settings import BaseSettings, SettingsConfigDict

APP_NAME = "E-commerce Admin AI Assistant"


class Settings(BaseSettings):
    debug: bool = False
    database_url: str
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"
    openai_embedding_model: str = "text-embedding-3-small"
    openai_embedding_dimension: int = 1536

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()
