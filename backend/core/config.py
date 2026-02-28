import os

from pydantic_settings import BaseSettings, SettingsConfigDict

_HERE = os.path.dirname(os.path.abspath(__file__))
_BACKEND = os.path.dirname(_HERE)
_DATA = os.path.join(_BACKEND, "data")


class Settings(BaseSettings):
    gemini_api_key: str
    temporal_host: str = "localhost:7233"
    db_path: str = os.path.join(_DATA, "game.db")
    index_dir: str = os.path.join(_DATA, "indexes")
    active_scenario: str = "ashwood"

    model_config = SettingsConfigDict(env_file=os.path.join(_BACKEND, ".env"))

    def for_scenario(self, scenario_id: str) -> "Settings":
        return self.model_copy(update={
            "db_path": os.path.join(_DATA, f"{scenario_id}.db"),
            "index_dir": os.path.join(_DATA, "indexes", scenario_id),
            "active_scenario": scenario_id,
        })
