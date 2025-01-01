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
