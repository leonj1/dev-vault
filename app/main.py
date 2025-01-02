from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
import logging
import os
from typing import List
from .models import Secret, Project
from .services.projects_service import ProjectsService

app = FastAPI(
    title="Secrets API",
    description="API for managing secrets",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Get absolute path to static directory
current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir, "static")
logger.debug(f"Static directory path: {static_dir}")

@app.get("/")
async def root():
    with open(os.path.join(static_dir, "index.html"), "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)

# Create single instance of ProjectsService
projects_service = ProjectsService()

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

@app.post("/projects/{identifier}/secrets", response_model=Project)
async def create_secret(
    identifier: str,
    secret: Secret,
    service: ProjectsService = Depends(get_projects_service)
) -> Project:
    """Create a new secret in a project"""
    project = await service.create_secret(identifier, secret)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@app.get("/projects/{identifier}/secrets", response_model=List[Secret])
async def list_project_secrets(
    identifier: str,
    service: ProjectsService = Depends(get_projects_service)
) -> List[Secret]:
    """List all secrets in a project"""
    secrets = await service.list_project_secrets(identifier)
    if secrets is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return secrets

@app.put("/projects/{identifier}/secrets/{secret_id}", response_model=Project)
async def update_secret(
    identifier: str,
    secret_id: str,
    secret: Secret,
    service: ProjectsService = Depends(get_projects_service)
) -> Project:
    """Update a secret in a project"""
    project = await service.update_secret(identifier, secret_id, secret)
    if not project:
        raise HTTPException(status_code=404, detail="Project or secret not found")
    return project

@app.delete("/projects/{identifier}/secrets/{secret_id}", response_model=Project)
async def delete_secret(
    identifier: str,
    secret_id: str,
    service: ProjectsService = Depends(get_projects_service)
) -> Project:
    """Delete a secret from a project"""
    project = await service.delete_secret(identifier, secret_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project
