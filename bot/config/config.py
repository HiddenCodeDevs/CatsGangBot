from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

    API_ID: int
    API_HASH: str
    DO_CHANNELS_TASKS: bool = False

    REF_ID: str = ''

    USE_PROXY_FROM_FILE: bool = False


settings = Settings()


