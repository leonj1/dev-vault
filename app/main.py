from fastapi import FastAPI, HTTPException, Depends
from typing import List
from .models import Secret, Project
from .services.secrets_service import SecretsService
from .services.projects_service import ProjectsService

app = FastAPI(
    title="Secrets API",
    description="API for managing secrets",
    version="1.0.0"
)

# Create single instances of services
secrets_service = SecretsService()
projects_service = ProjectsService()

def get_secrets_service() -> SecretsService:
    """
    Dependency injection for SecretsService.

    Returns:
        Instance of SecretsService
    """
    return secrets_service

def get_projects_service() -> ProjectsService:
    """
    Dependency injection for ProjectsService.

    Returns:
        Instance of ProjectsService
    """
    return projects_service

@app.post("/projects/", response_model=Project)
async def create_project(
    project: Project,
    service: ProjectsService = Depends(get_projects_service)
) -> Project:
    """Create a new project"""
    return await service.create_project(project)

@app.get("/projects/", response_model=List[Project])
async def list_projects(
    service: ProjectsService = Depends(get_projects_service)
) -> List[Project]:
    """List all projects"""
    return await service.list_projects()

@app.get("/projects/{identifier}", response_model=Project)
async def get_project(
    identifier: str,
    service: ProjectsService = Depends(get_projects_service)
) -> Project:
    """Get a project by identifier"""
    project = await service.get_project(identifier)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@app.put("/projects/{identifier}", response_model=Project)
async def update_project(
    identifier: str,
    project: Project,
    service: ProjectsService = Depends(get_projects_service)
) -> Project:
    """Update a project"""
    updated_project = await service.update_project(identifier, project)
    if not updated_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return updated_project

@app.delete("/projects/{identifier}", response_model=bool)
async def delete_project(
    identifier: str,
    service: ProjectsService = Depends(get_projects_service)
) -> bool:
    """Delete a project"""
    if not await service.delete_project(identifier):
        raise HTTPException(status_code=404, detail="Project not found")
    return True

@app.post("/secrets/", response_model=Secret)
async def create_secret(
    secret: Secret,
    service: SecretsService = Depends(get_secrets_service)
) -> Secret:
    return await service.create_secret(secret)

@app.get("/secrets/", response_model=List[Secret])
async def list_secrets(
    service: SecretsService = Depends(get_secrets_service)
) -> List[Secret]:
    return await service.list_secrets()

@app.post("/projects/{identifier}/secrets/{secret_id}", response_model=Project)
async def add_secret_to_project(
    identifier: str,
    secret_id: str,
    service: ProjectsService = Depends(get_projects_service),
    secrets_service: SecretsService = Depends(get_secrets_service)
) -> Project:
    """Add a secret to a project"""
    # Verify secret exists
    secrets = await secrets_service.list_secrets()
    if not any(s.identifier == secret_id for s in secrets):
        raise HTTPException(status_code=404, detail="Secret not found")
    
    # Add secret to project
    project = await service.add_secret(identifier, secret_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@app.delete("/projects/{identifier}/secrets/{secret_id}", response_model=Project)
async def delete_secret_from_project(
    identifier: str,
    secret_id: str,
    service: ProjectsService = Depends(get_projects_service)
) -> Project:
    """Delete a secret from a project"""
    project = await service.delete_secret(identifier, secret_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project
