import os

from pydantic_settings import BaseSettings, SettingsConfigDict

_HERE = os.path.dirname(os.path.abspath(__file__))
_BACKEND = os.path.dirname(_HERE)


class Settings(BaseSettings):
    gemini_api_key: str
    temporal_host: str = "localhost:7233"
    db_path: str = os.path.join(_BACKEND, "data", "game.db")
    index_dir: str = os.path.join(_BACKEND, "data", "indexes")

    model_config = SettingsConfigDict(env_file=os.path.join(_BACKEND, ".env"))
