from typing import List, Optional
from ..models import Project, Secret

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

    async def create_secret(self, project_id: str, secret: Secret) -> Optional[Project]:
        """
        Create a new secret in a project.

        Args:
            project_id: Project identifier
            secret: Secret to create

        Returns:
            Updated project if found, None otherwise
        """
        project = await self.get_project(project_id)
        if not project:
            return None
        project.secrets.append(secret)
        self._projects[project_id] = project
        return project

    async def list_project_secrets(self, project_id: str) -> Optional[List[Secret]]:
        """
        List all secrets in a project.

        Args:
            project_id: Project identifier

        Returns:
            List of secrets if project found, None otherwise
        """
        project = await self.get_project(project_id)
        if not project:
            return None
        return project.secrets

    async def update_secret(self, project_id: str, secret_id: str, secret: Secret) -> Optional[Project]:
        """
        Update a secret in a project.

        Args:
            project_id: Project identifier
            secret_id: Secret identifier to update
            secret: Updated secret data

        Returns:
            Updated project if found and secret updated, None otherwise
        """
        project = await self.get_project(project_id)
        if not project:
            return None

        for i, existing_secret in enumerate(project.secrets):
            if existing_secret.identifier == secret_id:
                secret.identifier = secret_id  # Ensure identifier remains the same
                project.secrets[i] = secret
                self._projects[project_id] = project
                return project
        return None

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

        original_length = len(project.secrets)
        project.secrets = [s for s in project.secrets if s.identifier != secret_id]
        if len(project.secrets) == original_length:
            return None  # Secret not found
        self._projects[project_id] = project
        return project
