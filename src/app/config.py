from dataclasses import dataclass
import os

@dataclass(frozen=True)
class Settings:
    database_path: str
    charts_output_dir: str

def get_settings() -> Settings:
    return Settings(
        database_path=os.environ["DATABASE_PATH"],
        charts_output_dir=os.environ["CHARTS_OUTPUT_DIR"]
    )
