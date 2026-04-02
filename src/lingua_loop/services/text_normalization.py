from abc import ABC
from abc import abstractmethod

from lingua_loop.integrations.youtube.types import SupportedLanguages


class TextNormalizer(ABC):
    @abstractmethod
    def normalize(self, text: str) -> str:
        raise NotImplementedError


class GenericNormalizer(TextNormalizer):
    """Default normalizer in case language supported but no specific impl"""

    def normalize(self, text: str) -> str:
        raise NotImplementedError


class GermanNormalizer(TextNormalizer):
    def normalize(self, text: str) -> str:
        # TODO: handle esset normalization ä -> ae, ü -> ue, ö -> oe, ß -> ss
        raise NotImplementedError


class TextNormalizerFactory:
    _languages = {SupportedLanguages.GERMAN: GermanNormalizer}

    def __call__(self, language: SupportedLanguages) -> TextNormalizer:
        normalizer_cls = self._languages.get(language, GenericNormalizer)
        return normalizer_cls()


text_normalizer_factory = TextNormalizerFactory()
