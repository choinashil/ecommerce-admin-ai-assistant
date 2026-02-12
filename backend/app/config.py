from pydantic_settings import BaseSettings, SettingsConfigDict

APP_NAME = "E-commerce Admin AI Assistant"


class Settings(BaseSettings):
    debug: bool = False
    database_url: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()
