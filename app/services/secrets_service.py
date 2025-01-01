from typing import List
from ..models import Secret

class SecretsService:
    def __init__(self):
        self._secrets: List[Secret] = []

    async def create_secret(self, secret: Secret) -> Secret:
        """
        Create a new secret.

        Args:
            secret: The secret to create

        Returns:
            The created secret
        """
        self._secrets.append(secret)
        return secret

    async def list_secrets(self) -> List[Secret]:
        """
        List all secrets.

        Returns:
            List of all secrets
        """
        return self._secrets

    async def update_secret(self, identifier: str, secret: Secret) -> Secret:
        """
        Update a secret.

        Args:
            identifier: The identifier of the secret to update
            secret: The updated secret data

        Returns:
            Updated secret if found, None otherwise
        """
        for i, existing_secret in enumerate(self._secrets):
            if existing_secret.identifier == identifier:
                secret.identifier = identifier  # Ensure identifier remains the same
                self._secrets[i] = secret
                return secret
        return None

    async def delete_secret(self, identifier: str) -> bool:
        """
        Delete a secret.

        Args:
            identifier: The identifier of the secret to delete

        Returns:
            True if secret was deleted, False if not found
        """
        for i, secret in enumerate(self._secrets):
            if secret.identifier == identifier:
                self._secrets.pop(i)
                return True
        return False
