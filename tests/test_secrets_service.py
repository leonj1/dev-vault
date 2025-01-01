import pytest
from app.models import Secret, Source
from app.services.secrets_service import SecretsService

@pytest.fixture
def service():
    return SecretsService()

@pytest.mark.asyncio
async def test_create_secret(service):
    test_cases = [
        {
            "name": "test-secret",
            "source": Source.AWS_SAM,
        },
        {
            "name": "another-secret",
            "source": Source.OTHER,
        }
    ]

    for case in test_cases:
        secret = Secret(**case)
        result = await service.create_secret(secret)
        assert result.name == case["name"]
        assert result.source == case["source"]
        assert result.identifier is not None

@pytest.mark.asyncio
async def test_list_secrets(service):
    # Create test secrets
    secrets = [
        Secret(name="secret1", source=Source.AWS_SAM),
        Secret(name="secret2", source=Source.OTHER)
    ]
    
    for secret in secrets:
        await service.create_secret(secret)
    
    # Test listing
    result = await service.list_secrets()
    assert len(result) == len(secrets)
    assert all(isinstance(s, Secret) for s in result)
