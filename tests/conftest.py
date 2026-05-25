import copy
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture(scope="function")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(autouse=True)
def reset_activities():
    """Save and restore the in-memory activities dict around each test."""
    orig = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(copy.deepcopy(orig))
