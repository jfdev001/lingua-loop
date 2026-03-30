"""Database tests must use in memory dataset."""

import pytest

from tests.config import ENV_DATABASE_PATH
from tests.config import IN_MEMORY


@pytest.fixture(scope="session", autouse=True)
def unit_db():
    # TODO: populate with some example data corresponding to the desired models
    assert False  # not implemented... should create in memory dataset and populate?
    # monkeypatch.setenv(ENV_DATABASE_PATH, IN_MEMORY)
    return
