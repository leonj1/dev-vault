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
        # Initialize empty secrets list if none provided
        if project.secrets is None:
            project.secrets = []
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

    async def add_secret(self, project_id: str, secret_id: str) -> Optional[Project]:
        """
        Add a secret to a project.

        Args:
            project_id: Project identifier
            secret_id: Secret identifier to add

        Returns:
            Updated project if found, None otherwise
        """
        project = await self.get_project(project_id)
        if not project:
            return None
        if secret_id not in project.secrets:
            project.secrets.append(secret_id)
            self._projects[project_id] = project  # Save the updated project
        return project

    async def delete_secret(self, project_id: str, secret_id: str) -> Optional[Project]:
        """
        Delete a secret from a project.

        Args:
            project_id: Project identifier
            secret_id: Secret identifier to remove

        Returns:
            Updated project if found and secret removed, None otherwise
        """
        project = await self.get_project(project_id)
        if not project:
            return None
        if secret_id in project.secrets:
            project.secrets.remove(secret_id)
            self._projects[project_id] = project  # Save the updated project
        return project
