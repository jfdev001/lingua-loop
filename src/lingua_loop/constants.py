from pathlib import Path

# Directories
BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = Path(__file__).resolve().parents[2]
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"

# Database
DATABASE_DIR = "data"
TRANSCRIPTS_DB = "transcripts.db"
DEFAULT_DATABASE_PATH = PROJECT_DIR / DATABASE_DIR / TRANSCRIPTS_DB
DEFAULT_DB_DRIVER = "sqlite+aiosqlite"

# Score consts
MAX_SCORE = 1.0
MIN_SCORE = 0.0
