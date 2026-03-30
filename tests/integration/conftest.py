# TODO: just run the tests separately... and initialize the dbs here...
from os import environ

import pytest
from pytest import exit

from tests.config import ENV_DATABASE_PATH
from tests.config import ENV_INTEGRATION_TEST
from tests.config import ENV_UNIT_TEST
from tests.config import TEST_ON

environ[ENV_INTEGRATION_TEST] = TEST_ON

if environ[ENV_UNIT_TEST] == TEST_ON:
    exit("integration and unit tests cannot run at same time due to database")


@pytest.fixture(scope="session", autouse=True)
def integration_db():
    assert False  # not implemented.. should create table though??? depends
    # on what you need right...
    # monkeypatch.setenv(ENV_DATABASE_PATH, str(TEST_DATABASE_PATH))
    return
