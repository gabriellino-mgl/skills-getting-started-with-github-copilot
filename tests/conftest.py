import importlib

import pytest
from fastapi.testclient import TestClient
from src import app as app_module


@pytest.fixture
def client():
    app = importlib.reload(app_module)
    return TestClient(app.app)
