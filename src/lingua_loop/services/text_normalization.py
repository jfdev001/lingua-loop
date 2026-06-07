"""Text normalization utilities for scoring comparisons."""

from abc import ABC
from abc import abstractmethod
from re import sub
from typing import Literal
from unicodedata import combining
from unicodedata import normalize

from lingua_loop.integrations.youtube.types import SupportedLanguageCodes

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
        """Normalize text through all normalization steps."""
        text = self.normalize_special_characters(text)
        text = self.normalize_case(text)
        text = self.normalize_punctuation(text)
        text = self.normalize_whitespace(text)
        return text

    @abstractmethod
    def normalize_special_characters(self, text: str) -> str:
        """Replace or remove special characters (return text if no change).

        In some languages, like German, special characters like "ß" can be
        noramalized to written as "ss" and this does not change meaning.
        However, for languages like Italian, there is a difference between "è"
        and "e", so no special characters normalization is implemented for
        that.
        """
        pass

    def normalize_case(self, text: str) -> str:
        """Normalize text to lowercase."""
        return text.lower()

    def normalize_punctuation(self, text: str) -> str:
        """Remove punctuation from text."""
        all_chars_except_words_and_single_spaces = r"[^\w\s]"
        space = " "
        return sub(
            pattern=all_chars_except_words_and_single_spaces,
            repl=space,
            string=text,
        )

    def normalize_whitespace(self, text: str) -> str:
        """Collapse whitespace and strip."""
        one_or_more_spaces = r"\s+"
        space = " "
        return sub(pattern=one_or_more_spaces, repl=space, string=text).strip()


class GenericNormalizer(TextNormalizer):
    """Normalizer that performs no special character normalization."""

    def normalize_special_characters(self, text: str) -> str:
        """Return text unchanged."""
        return text


class DutchNormalizer(TextNormalizer):
    """Normalizer for Dutch text."""

    def normalize_special_characters(self, text: str) -> str:
        """Remove combining characters via NFKD normalization."""
        text = normalize(self.form, text)
        text = "".join(c for c in text if not combining(c))
        return text


class GermanNormalizer(TextNormalizer):
    """Normalizer for German text."""

    def normalize_special_characters(self, text: str) -> str:
        """Replace German special characters with ASCII equivalents."""
        text = (
            text.replace("ß", "ss")
            .replace("ä", "ae")
            .replace("ö", "oe")
            .replace("ü", "ue")
        )
        return text


class TextNormalizerFactory:
    """Factory for creating appropriate TextNormalizer instances."""

    _language_code_to_normalizer = {
        SupportedLanguageCodes.DUTCH: DutchNormalizer,
        SupportedLanguageCodes.GERMAN: GermanNormalizer,
    }

    def __call__(self, language_code: SupportedLanguageCodes) -> TextNormalizer:
        """Get the appropriate normalizer for the given language code."""
        normalizer_cls = self._language_code_to_normalizer.get(
            language_code, GenericNormalizer
        )
        return normalizer_cls()


text_normalizer_factory = TextNormalizerFactory()
