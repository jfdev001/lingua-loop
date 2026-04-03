from enum import Enum
from typing import Dict


class SupportedLanguageCodes(str, Enum):
    DUTCH = "nl"
    ENGLISH = "en"
    GERMAN = "de"
    ITALIAN = "it"


class SupportedLanguages(str, Enum):
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
