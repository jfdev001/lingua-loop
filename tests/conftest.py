import pytest
from starlette.testclient import TestClient

from lingua_loop.main import app


@pytest.fixture(scope="module")
def test_api():
    """Fixture for testing API (i.e., no temporary DB needed)"""
    client = TestClient(app)
    yield client


@pytest.fixture
def test_crud():
    """Fixtures for testing temporary DB"""
    pass
