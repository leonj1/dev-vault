import pytest
from fastapi.testclient import TestClient
from app.main import app, get_projects_service
from app.models import Source

@pytest.fixture
def client(projects_service):
    app.dependency_overrides[get_projects_service] = lambda: projects_service
    return TestClient(app)

def test_create_project(client):
    test_cases = [
        {
            "name": "test-project",
            "secrets": []
        },
        {
            "name": "another-project",
            "secrets": []  # Projects start with no secrets
        }
    ]

    for case in test_cases:
        response = client.post("/projects/", json=case)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == case["name"]
        assert isinstance(data["secrets"], list)
        assert len(data["secrets"]) == 0
        assert "identifier" in data

def test_list_projects(client):
    # Create test projects
    projects = [
        {"name": "project1", "secrets": []},
        {"name": "project2", "secrets": []}
    ]
    
    created_projects = []
    for project in projects:
        response = client.post("/projects/", json=project)
        assert response.status_code == 200
        created_projects.append(response.json())
    
    # Test listing
    response = client.get("/projects/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(projects)
    assert all("name" in p and "secrets" in p and "identifier" in p for p in data)

def test_get_project(client):
    # Create a project
    project_data = {"name": "test-project", "secrets": []}
    create_response = client.post("/projects/", json=project_data)
    assert create_response.status_code == 200
    created_project = create_response.json()
    
    # Test getting the project
    response = client.get(f"/projects/{created_project['identifier']}")
    assert response.status_code == 200
    data = response.json()
    assert data == created_project
    
    # Test getting non-existent project
    response = client.get("/projects/non-existent")
    assert response.status_code == 404

def test_update_project(client):
    # Create a project
    project_data = {"name": "test-project", "secrets": []}
    create_response = client.post("/projects/", json=project_data)
    assert create_response.status_code == 200
    created_project = create_response.json()
    
    # Update the project name (secrets should be managed through secret endpoints)
    updated_data = {
        "name": "updated-project",
        "secrets": []
    }
    response = client.put(
        f"/projects/{created_project['identifier']}", 
        json=updated_data
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == updated_data["name"]
    assert data["identifier"] == created_project["identifier"]
    
    # Test updating non-existent project
    response = client.put("/projects/non-existent", json=updated_data)
    assert response.status_code == 404

def test_delete_project(client):
    # Create a project
    project_data = {"name": "test-project", "secrets": []}
    create_response = client.post("/projects/", json=project_data)
    assert create_response.status_code == 200
    created_project = create_response.json()
    
    # Delete the project
    response = client.delete(f"/projects/{created_project['identifier']}")
    assert response.status_code == 200
    assert response.json() is True
    
    # Verify project is deleted
    get_response = client.get(f"/projects/{created_project['identifier']}")
    assert get_response.status_code == 404
    
    # Test deleting non-existent project
    response = client.delete("/projects/non-existent")
    assert response.status_code == 404

def test_complete_project_secret_flow(client):
    """Test the complete flow of project and secret management:
    1. Create a project
    2. Add a secret to the project
    3. Update the secret
    4. Remove the secret
    5. Verify project has no secrets
    """
    # 1. Create a project
    project_data = {
        "name": "flow-test-project",
        "secrets": []
    }
    project_response = client.post("/projects/", json=project_data)
    assert project_response.status_code == 200
    project = project_response.json()
    assert len(project["secrets"]) == 0
    
    # 2. Add a secret to the project
    secret_data = {
        "name": "flow-test-secret",
        "value": "test-value",
        "source": Source.AWS_SAM.value
    }
    secret_response = client.post(
        f"/projects/{project['identifier']}/secrets",
        json=secret_data
    )
    assert secret_response.status_code == 200
    updated_project = secret_response.json()
    assert len(updated_project["secrets"]) == 1
    secret = updated_project["secrets"][0]
    assert secret["name"] == secret_data["name"]
    
    # 3. Update the secret
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
    updated_project = update_response.json()
    updated_secret = updated_project["secrets"][0]
    assert updated_secret["name"] == updated_secret_data["name"]
    
    # 4. Remove the secret
    remove_response = client.delete(
        f"/projects/{project['identifier']}/secrets/{secret['identifier']}"
    )
    assert remove_response.status_code == 200
    final_project = remove_response.json()
    
    # 5. Verify project has no secrets
    assert len(final_project["secrets"]) == 0
    
    # Double-check by getting the project directly
    get_response = client.get(f"/projects/{project['identifier']}")
    assert get_response.status_code == 200
    retrieved_project = get_response.json()
    assert len(retrieved_project["secrets"]) == 0
