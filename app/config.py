from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_url: str
    secret_key: str
    base_url: str
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
