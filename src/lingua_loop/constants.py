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
DATABASE_DIR = "db"
DEFAULT_ENV_DATABASE_PATH = BASE_DIR / DATABASE_DIR / TRANSCRIPTS_DB
DEFAULT_ENV_DB_DRIVER = "sqlite+aiosqlite"

# Score consts
MAX_SCORE = 1.0
MIN_SCORE = 0.0
