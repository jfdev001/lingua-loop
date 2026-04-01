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

# Data
TEST_VIDEO_ID = "tageschau"
N_SEGMENTS_IN_TEST_TRANSCRIPT = 3
TAGESSCHAU_VID_OFFICIAL = "_RoFnUnT060"
