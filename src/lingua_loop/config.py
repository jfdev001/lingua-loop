from pathlib import Path
from enum import Enum
from os import getenv, environ

# Environment variable names
ENV_DATABASE_PATH = "DATABASE_PATH"
ENV_DB_DRIVER = "DB_DRIVER"

# Directories
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"

# Testing
# TODO: this shouldn't live here... but basically prevents unit and
# integration tests from running at the same time
TEST_ON = "ON"
TEST_OFF = "OFF"
ENV_UNIT_TEST = "UNIT_TEST"
DEFAULT_ENV_UNIT_TEST = TEST_OFF
environ[ENV_UNIT_TEST] = DEFAULT_ENV_UNIT_TEST

ENV_INTEGRATION_TEST = "INTEGRATION_TEST"
DEFAULT_ENV_INTEGRATION_TEST = TEST_OFF
environ[ENV_INTEGRATION_TEST] = DEFAULT_ENV_INTEGRATION_TEST

IN_MEMORY = ":memory:"
TEST_DB = "test.db"
TEST_DATABASE_PATH = BASE_DIR / TEST_DB

# Database
# NOTE: BASE_DIR coudl also be configurable if changing DBs

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
