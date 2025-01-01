import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models import Source

client = TestClient(app)

def test_create_secret():
    test_cases = [
        {
            "name": "test-secret",
            "source": Source.AWS_SAM.value,
        },
        {
            "name": "another-secret",
            "source": Source.OTHER.value,
        }
    ]

    for case in test_cases:
        response = client.post("/secrets/", json=case)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == case["name"]
        assert data["source"] == case["source"]
        assert "identifier" in data

def test_list_secrets():
    # Create test secrets
    secrets = [
        {"name": "secret1", "source": Source.AWS_SAM.value},
        {"name": "secret2", "source": Source.OTHER.value}
    ]
    
    for secret in secrets:
        client.post("/secrets/", json=secret)
    
    # Test listing
    response = client.get("/secrets/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert all("name" in s and "source" in s and "identifier" in s for s in data)
