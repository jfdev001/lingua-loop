from os import environ

from pytest import exit

from tests.config import ENV_INTEGRATION_TEST
from tests.config import ENV_UNIT_TEST
from tests.config import TEST_ON

environ[ENV_UNIT_TEST] = TEST_ON

# TODO: you can remove this... just put the fixtures for the databases
# in the module scope of integration/... and unit/db/...
# if environ[ENV_INTEGRATION_TEST] == TEST_ON:
#     exit("integration and unit tests cannot run at same time due to database")
