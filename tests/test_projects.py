import pytest
from fastapi.testclient import TestClient
from app.main import app, get_projects_service

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
            "secrets": ["secret1", "secret2"]
        }
    ]

    for case in test_cases:
        response = client.post("/projects/", json=case)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == case["name"]
        assert data["secrets"] == case["secrets"]
        assert "identifier" in data

def test_list_projects(client):
    # Create test projects
    projects = [
        {"name": "project1", "secrets": []},
        {"name": "project2", "secrets": ["secret1"]}
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
    
    # Update the project
    updated_data = {
        "name": "updated-project",
        "secrets": ["secret1"]
    }
    response = client.put(
        f"/projects/{created_project['identifier']}", 
        json=updated_data
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == updated_data["name"]
    assert data["secrets"] == updated_data["secrets"]
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
