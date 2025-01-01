import os
import sys
from pathlib import Path

# Add the project root directory to Python path
project_root = str(Path(__file__).parent.parent.absolute())
sys.path.insert(0, project_root)

import pytest
from app.services.secrets_service import SecretsService

@pytest.fixture(scope="session")
def secrets_service():
    return SecretsService()

@pytest.fixture(autouse=True)
def clear_secrets(secrets_service):
    """Clear secrets before each test."""
    secrets_service._secrets.clear()
    yield
    secrets_service._secrets.clear()
