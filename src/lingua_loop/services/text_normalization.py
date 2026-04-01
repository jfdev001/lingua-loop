from abc import ABC
from abc import abstractmethod
from typing import List

from lingua_loop.db.models import Segment
from lingua_loop.integrations.youtube.types import SupportedLanguages


def normalize(text: str, language: SupportedLanguages) -> List[Segment]:
    """ """
    if language == SupportedLanguages.GERMAN:
        # TODO: handle esset normalization ä -> ae, ü -> ue, ö -> oe, ß -> ss
        raise NotImplementedError
    raise NotImplemented


# TODO: better to take factory/abstract approach here for extending to
# different langs


class TextNormalizer(ABC):
    @abstractmethod
    def normalize(self, text: str):
        raise NotImplementedError


class GenericNormalizer(TextNormalizer):
    """Default normalizer in case language supported but no specific impl"""

    pass


class GermanNormalizer(TextNormalizer):
    pass


class TextNormalizerFactory:
    pass
