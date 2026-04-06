from pathlib import Path

# Directories
BASE_DIR = Path(__file__).resolve().parent
HOME_DIR = Path.home()
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"

# Database
DATABASE_DIR_BASENAME = ".lingua_loop"
DATABASE_DIR = HOME_DIR / DATABASE_DIR_BASENAME
TRANSCRIPTS_DB = "transcripts.db"
DEFAULT_DATABASE_PATH = DATABASE_DIR / TRANSCRIPTS_DB
DEFAULT_DB_DRIVER = "sqlite+aiosqlite"

# Score consts
MAX_SCORE = 1.0
MIN_SCORE = 0.0
