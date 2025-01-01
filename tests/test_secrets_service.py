import pytest
from app.models import Secret, Source

@pytest.mark.asyncio
async def test_create_secret(secrets_service):
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
        result = await secrets_service.create_secret(secret)
        assert result.name == case["name"]
        assert result.source == case["source"]
        assert result.identifier is not None

@pytest.mark.asyncio
async def test_list_secrets(secrets_service):
    # Create test secrets
    secrets = [
        Secret(name="secret1", source=Source.AWS_SAM),
        Secret(name="secret2", source=Source.OTHER)
    ]
    
    initial_count = len(await secrets_service.list_secrets())
    assert initial_count == 0, "Secrets should be empty at start of test"
    
    for secret in secrets:
        await secrets_service.create_secret(secret)
    
    # Test listing
    result = await secrets_service.list_secrets()
    assert len(result) == len(secrets)
    assert all(isinstance(s, Secret) for s in result)
