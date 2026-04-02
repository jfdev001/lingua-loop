from abc import ABC
from abc import abstractmethod
from re import sub
from typing import Literal

from lingua_loop.integrations.youtube.types import SupportedLanguages

NormalizationForm = Literal["NFC", "NFKC", "NFD", "NFKD"]


class TextNormalizer(ABC):
    """Normalizes text for comparison/scoring purposes.

    The normalization is intentionally lossy and removes distinctions such as:
    - (language-specific) accent variations
    - case differences
    - punctuation

    As a result, texts like "Er hat gesagt" and "er hat gesagt"
    are considered equivalent after normalization.
    """

    form: NormalizationForm = "NFKD"

    def normalize(self, text: str) -> str:
        text = self.normalize_accents(text)
        text = self.normalize_case(text)
        text = self.normalize_punctuation(text)
        text = self.normalize_whitespace(text)
        return text

    @abstractmethod
    def normalize_accents(self, text: str) -> str:
        """Replace accents (return text if no change)"""
        pass

    def normalize_case(self, text: str) -> str:
        return text.lower()

    def normalize_punctuation(self, text: str) -> str:
        all_chars_except_words_and_single_spaces = r"[^\w\s]"
        space = " "
        return sub(
            pattern=all_chars_except_words_and_single_spaces,
            repl=space,
            string=text,
        )

    def normalize_whitespace(self, text: str) -> str:
        more_than_one_space = r"\s+"
        space = " "
        return sub(pattern=more_than_one_space, repl=space, string=text).strip()


class GenericNormalizer(TextNormalizer):
    def normalize_accents(self, text: str) -> str:
        return text


class GermanNormalizer(TextNormalizer):
    def normalize_accents(self, text: str) -> str:
        text = (
            text.replace("ß", "ss")
            .replace("ä", "ae")
            .replace("ö", "oe")
            .replace("ü", "ue")
        )
        return text


class TextNormalizerFactory:
    _languages = {SupportedLanguages.GERMAN: GermanNormalizer}

    def __call__(self, language: SupportedLanguages) -> TextNormalizer:
        normalizer_cls = self._languages.get(language, GenericNormalizer)
        return normalizer_cls()


text_normalizer_factory = TextNormalizerFactory()
