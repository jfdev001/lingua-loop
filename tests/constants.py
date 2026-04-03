from pathlib import Path

# Unit/integration environment variables
TEST_ON = "ON"
TEST_OFF = "OFF"

ENV_UNIT_TEST = "UNIT_TEST"
ENV_INTEGRATION_TEST = "INTEGRATION_TEST"
DEFAULT_ENV_INTEGRATION_TEST = TEST_OFF

# Database
IN_MEMORY = ":memory:?cache=shared"
TEST_DIR = Path(__file__).resolve().parent
TEST_DB = "test.db"
TEST_DATABASE_PATH = str(TEST_DIR / TEST_DB)

# Unit test data
TEST_VIDEO_ID = "tageschau"
N_SEGMENTS_IN_TEST_TRANSCRIPT = 3

TAGESSCHAU_VIDEO_ID = "_RoFnUnT060"
N_MOCKED_SEGMENTS = 3

# Integration test data
INTEGRATION_ENGLISH_VIDEO_ID = "abc123"
INTEGRATION_GERMAN_VIDEO_ID = "hallo_leute"
