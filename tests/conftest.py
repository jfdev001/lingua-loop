import pytest
from starlette.testclient import TestClient

from lingua_loop.main import app


@pytest.fixture(scope="module")
def test_api():
    """Fixture for testing API... really should have temp DB here to ensure
    the API touches the DB as intended


    References:
        * good overall example of testing https://testdriven.io/blog/fastapi-crud/, though
        does not use in memory dataset
        * bali uses in memory, so does forecast in a box 
    """
    client = TestClient(app)
    yield client


@pytest.fixture
def test_crud():
    """Fixtures for testing temporary DB (this should just be raw low level
    adds like db.session.add(....) to see what the results are???

    You can just drop this test here tbh...

    Consider also in memory dataset, see e.g., 
    https://github.com/bali-framework/bali

    Maybe need 
    https://sqlmodel.tiangolo.com/tutorial/fastapi/tests/#create-the-engine-and-session-for-testing
    """
    raise NotImplementedError()
