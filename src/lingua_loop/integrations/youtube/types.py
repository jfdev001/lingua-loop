"""YouTube integration type definitions."""

from enum import Enum
from typing import Dict


class SupportedLanguageCodes(str, Enum):
    """Supported language codes for YouTube transcripts."""

    DUTCH = "nl"
    ENGLISH = "en"
    GERMAN = "de"
    ITALIAN = "it"


class SupportedLanguages(str, Enum):
    """Human-readable language names."""

    DUTCH = "Dutch"
    ENGLISH = "English"
    GERMAN = "German"
    ITALIAN = "Italian"


language_code_to_language: Dict[SupportedLanguageCodes, SupportedLanguages] = {
    language_code: language
    for language_code, language in zip(
        SupportedLanguageCodes, SupportedLanguages
    )
}
