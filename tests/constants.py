from pathlib import Path

# Database
IN_MEMORY = ":memory:?cache=shared"
TEST_DIR = Path(__file__).resolve().parent
TEST_DB = "test.db"
TEST_DATABASE_PATH = str(TEST_DIR / TEST_DB)

# All transcript segment info for dummy transcripts
N_SEGMENTS_IN_TEST_TRANSCRIPT = 3

# Unit test data
TEST_VIDEO_ID = "tageschau"
TAGESSCHAU_VIDEO_ID = "_RoFnUnT060"

# Integration test data
INTEGRATION_ENGLISH_VIDEO_ID = "abc123"
INTEGRATION_GERMAN_VIDEO_ID = "hallo_leute"
