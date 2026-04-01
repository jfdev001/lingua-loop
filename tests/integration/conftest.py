from os import environ
from os import getenv

from pytest import exit

from tests.constants import ENV_INTEGRATION_TEST
from tests.constants import ENV_UNIT_TEST
from tests.constants import TEST_ON

environ[ENV_INTEGRATION_TEST] = TEST_ON

if getenv(ENV_UNIT_TEST, None) == TEST_ON:
    exit("integration and unit tests cannot run at same time due to database")
