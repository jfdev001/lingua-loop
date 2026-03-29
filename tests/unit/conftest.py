from os import environ
from pytest import exit
from lingua_loop.config import ENV_UNIT_TEST, ENV_INTEGRATION_TEST, TEST_ON
environ[ENV_UNIT_TEST] = TEST_ON

if environ[ENV_INTEGRATION_TEST] == TEST_ON:
    exit("integration and unit tests cannot run at same time due to database")
