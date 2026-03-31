from os import environ

from pytest import exit

from tests.config import ENV_INTEGRATION_TEST
from tests.config import ENV_UNIT_TEST
from tests.config import TEST_ON

environ[ENV_UNIT_TEST] = TEST_ON

if environ[ENV_INTEGRATION_TEST] == TEST_ON:
    exit("integration and unit tests cannot run at same time due to database")
