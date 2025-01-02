import pytest
from fastapi.testclient import TestClient
from app.main import app, get_projects_service
from app.models import Source

@pytest.fixture
def client(projects_service):
    app.dependency_overrides[get_projects_service] = lambda: projects_service
    return TestClient(app)

def test_project_secret_management(client):
    test_cases = [
        {
            "name": "Test project with multiple secrets",
            "project": {"name": "test-project", "secrets": []},
            "secrets": [
                {"name": "secret1", "value": "value1", "source": Source.AWS_SAM.value},
                {"name": "secret2", "value": "value2", "source": Source.OTHER.value}
            ],
            "expected_count": 2
        },
        {
            "name": "Test project with no secrets",
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

        # Create secrets in project
        created_secrets = []
        for secret_data in case["secrets"]:
            # Create secret
            secret_response = client.post(
                f"/projects/{project['identifier']}/secrets",
                json=secret_data
            )
            assert secret_response.status_code == 200
            updated_project = secret_response.json()
            assert len(updated_project["secrets"]) == len(created_secrets) + 1
            created_secrets.append(updated_project["secrets"][-1])

        # Test getting project secrets
        response = client.get(f"/projects/{project['identifier']}/secrets")
        assert response.status_code == 200
        secrets = response.json()
        
        # Verify response
        assert len(secrets) == case["expected_count"]
        if case["expected_count"] > 0:
            assert all(
                "name" in s and
                "value" in s and
                "source" in s and
                "identifier" in s
                for s in secrets
            )
            # Verify secret data matches what was created
            for created, retrieved in zip(created_secrets, secrets):
                assert created["name"] == retrieved["name"]
                assert created["value"] == retrieved["value"]
                assert created["source"] == retrieved["source"]

def test_update_project_secret(client):
    # Create project
    project_response = client.post("/projects/", json={"name": "test-project", "secrets": []})
    assert project_response.status_code == 200
    project = project_response.json()

    # Create secret
    secret_data = {"name": "test-secret", "value": "old-value", "source": Source.AWS_SAM.value}
    secret_response = client.post(
        f"/projects/{project['identifier']}/secrets",
        json=secret_data
    )
    assert secret_response.status_code == 200
    updated_project = secret_response.json()
    secret = updated_project["secrets"][0]

    # Update secret
    updated_secret_data = {
        "name": "updated-secret",
        "value": "new-value",
        "source": Source.OTHER.value
    }
    update_response = client.put(
        f"/projects/{project['identifier']}/secrets/{secret['identifier']}",
        json=updated_secret_data
    )
    assert update_response.status_code == 200
    final_project = update_response.json()
    updated_secret = final_project["secrets"][0]

    # Verify update
    assert updated_secret["name"] == updated_secret_data["name"]
    assert updated_secret["value"] == updated_secret_data["value"]
    assert updated_secret["source"] == updated_secret_data["source"]
    assert updated_secret["identifier"] == secret["identifier"]

def test_delete_project_secret(client):
    # Create project
    project_response = client.post("/projects/", json={"name": "test-project", "secrets": []})
    assert project_response.status_code == 200
    project = project_response.json()

    # Create secret
    secret_data = {"name": "test-secret", "value": "test-value", "source": Source.AWS_SAM.value}
    secret_response = client.post(
        f"/projects/{project['identifier']}/secrets",
        json=secret_data
    )
    assert secret_response.status_code == 200
    updated_project = secret_response.json()
    secret = updated_project["secrets"][0]

    # Delete secret
    delete_response = client.delete(
        f"/projects/{project['identifier']}/secrets/{secret['identifier']}"
    )
    assert delete_response.status_code == 200
    final_project = delete_response.json()
    assert len(final_project["secrets"]) == 0

def test_error_cases(client):
    # Test getting secrets for non-existent project
    response = client.get("/projects/non-existent/secrets")
    assert response.status_code == 404

    # Create project for other tests
    project_response = client.post("/projects/", json={"name": "test-project", "secrets": []})
    assert project_response.status_code == 200
    project = project_response.json()

    # Test updating non-existent secret
    update_response = client.put(
        f"/projects/{project['identifier']}/secrets/non-existent",
        json={"name": "test", "value": "test", "source": Source.AWS_SAM.value}
    )
    assert update_response.status_code == 404

    # Test deleting non-existent secret
    delete_response = client.delete(
        f"/projects/{project['identifier']}/secrets/non-existent"
    )
    assert delete_response.status_code == 404
