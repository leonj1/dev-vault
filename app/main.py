from fastapi import FastAPI, HTTPException, Depends
from typing import List
from .models import Secret
from .services.secrets_service import SecretsService

app = FastAPI(
    title="Secrets API",
    description="API for managing secrets",
    version="1.0.0"
)

# Create a single instance of SecretsService
secrets_service = SecretsService()

def get_secrets_service() -> SecretsService:
    """
    Dependency injection for SecretsService.

    Returns:
        Instance of SecretsService
    """
    return secrets_service

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
