import pytest
from fastapi.testclient import TestClient
from app.main import app, get_secrets_service
from app.models import Source

@pytest.fixture
def client(secrets_service):
    app.dependency_overrides[get_secrets_service] = lambda: secrets_service
    return TestClient(app)

def test_create_secret(client):
    test_cases = [
        {
            "name": "test-secret",
            "value": "test-value-1",
            "source": Source.AWS_SAM.value,
        },
        {
            "name": "another-secret",
            "value": "test-value-2",
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

def test_list_secrets(client):
    # Create test secrets
    secrets = [
        {"name": "secret1", "value": "value1", "source": Source.AWS_SAM.value},
        {"name": "secret2", "value": "value2", "source": Source.OTHER.value}
    ]
    
    for secret in secrets:
        response = client.post("/secrets/", json=secret)
        assert response.status_code == 200
    
    # Test listing
    response = client.get("/secrets/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert all("name" in s and "source" in s and "identifier" in s for s in data)

def test_get_project_secrets(client):
    test_cases = [
        {
            "name": "Test getting secrets for project with multiple secrets",
            "project": {"name": "test-project", "secrets": []},
            "secrets": [
                {"name": "secret1", "value": "value1", "source": Source.AWS_SAM.value},
                {"name": "secret2", "value": "value2", "source": Source.OTHER.value}
            ],
            "expected_count": 2
        },
        {
            "name": "Test getting secrets for project with no secrets",
            "project": {"name": "empty-project", "secrets": []},
            "secrets": [],
            "expected_count": 0
        }
    ]

    for case in test_cases:
        # Create project
        project_response = client.post("/projects/", json=case["project"])
        assert project_response.status_code == 200
        project = project_response.json()

        # Create secrets and add to project
        secret_ids = []
        for secret_data in case["secrets"]:
            # Create secret
            secret_response = client.post("/secrets/", json=secret_data)
            assert secret_response.status_code == 200
            secret = secret_response.json()
            secret_ids.append(secret["identifier"])

            # Add secret to project
            add_response = client.post(
                f"/projects/{project['identifier']}/secrets/{secret['identifier']}"
            )
            assert add_response.status_code == 200

        # Test getting project secrets
        response = client.get(f"/projects/{project['identifier']}/secrets")
        assert response.status_code == 200
        secrets = response.json()
        
        # Verify response
        assert len(secrets) == case["expected_count"]
        if case["expected_count"] > 0:
            assert all(
                s["identifier"] in secret_ids and
                "name" in s and
                "value" in s and
                "source" in s
                for s in secrets
            )

    # Test getting secrets for non-existent project
    response = client.get("/projects/non-existent/secrets")
    assert response.status_code == 404
