from typing import List, Optional
from ..models import Project

class ProjectsService:
    def __init__(self):
        self._projects = {}

    async def create_project(self, project: Project) -> Project:
        """
        Create a new project.

        Args:
            project: Project object to create

        Returns:
            Created project
        """
        self._projects[project.identifier] = project
        return project

    async def get_project(self, identifier: str) -> Optional[Project]:
        """
        Get a project by identifier.

        Args:
            identifier: Project identifier

        Returns:
            Project if found, None otherwise
        """
        return self._projects.get(identifier)

    async def list_projects(self) -> List[Project]:
        """
        List all projects.

        Returns:
            List of all projects
        """
        return list(self._projects.values())

    async def update_project(self, identifier: str, project: Project) -> Optional[Project]:
        """
        Update a project.

        Args:
            identifier: Project identifier
            project: Updated project data

        Returns:
            Updated project if found, None otherwise
        """
        if identifier not in self._projects:
            return None
        project.identifier = identifier
        self._projects[identifier] = project
        return project

    async def delete_project(self, identifier: str) -> bool:
        """
        Delete a project.

        Args:
            identifier: Project identifier

        Returns:
            True if project was deleted, False if not found
        """
        if identifier not in self._projects:
            return False
        del self._projects[identifier]
        return True
