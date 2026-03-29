# TODO: just run the tests separately... and initialize the dbs here...
import pytest

from lingua_loop.config import ENV_DATABASE_PATH, TEST_DATABASE_PATH

from os import environ
from pytest import exit
from lingua_loop.config import ENV_UNIT_TEST, ENV_INTEGRATION_TEST, TEST_ON
environ[ENV_INTEGRATION_TEST] = TEST_ON

if environ[ENV_UNIT_TEST] == TEST_ON:
    exit("integration and unit tests cannot run at same time due to database")


@pytest.fixture(scope="session", autouse=True)
def get_integration_db():
    assert False  # not implemented.. should create table though??? depends
    # on what you need right...
    # monkeypatch.setenv(ENV_DATABASE_PATH, str(TEST_DATABASE_PATH))
    return
