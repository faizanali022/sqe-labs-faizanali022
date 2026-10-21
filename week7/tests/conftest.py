import pytest
import auth

@pytest.fixture(autouse=True)
def fresh_store():
    auth.initialize_store()