from pathlib import Path
from enum import Enum


BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"


class SupportedLanguages(str, Enum):
    DUTCH = "nl"
    ENGLISH = "en"
    GERMAN = "de"
    ITALIAN = "it"
