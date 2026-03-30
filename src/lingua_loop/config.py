from enum import Enum
from os import environ
from os import getenv
from pathlib import Path

# Environment variable names
ENV_DATABASE_PATH = "DATABASE_PATH"
ENV_DB_DRIVER = "DB_DRIVER"

# Directories
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"

# Database
# NOTE: BASE_DIR could also be configurable if changing DBs

TRANSCRIPTS_DB = "transcripts.db"
DEFAULT_ENV_DATABASE_PATH = BASE_DIR / TRANSCRIPTS_DB
DATABASE_PATH = getenv(ENV_DATABASE_PATH, DEFAULT_ENV_DATABASE_PATH)

DEFAULT_ENV_DB_DRIVER = "sqlite+aiosqlite"
DB_DRIVER = getenv(ENV_DB_DRIVER, DEFAULT_ENV_DB_DRIVER)


class SupportedLanguages(str, Enum):
    DUTCH = "nl"
    ENGLISH = "en"
    GERMAN = "de"
    ITALIAN = "it"
