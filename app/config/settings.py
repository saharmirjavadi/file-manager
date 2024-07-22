from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    FM_MONGO_URI: str
    FM_MONGO_USER: str
    FM_MONGO_PASS: str
    FM_MONGO_DB: str
    FM_MONGO_COLLECTION: str
    FM_STORAGE_HOST: str
    FM_STORAGE_PORT: int
    FM_STORAGE_ACCESS_KEY: str
    FM_STORAGE_SECRET_KEY: str
    FM_TEMP_BUCKET: str
    FM_PERSIST_BUCKET: str

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True
    )


settings = Settings()
