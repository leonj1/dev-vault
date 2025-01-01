import pytest
from app.models import Secret, Source

@pytest.mark.asyncio
async def test_create_secret(secrets_service):
    test_cases = [
        {
            "name": "test-secret",
            "value": "test-value-1",
            "source": Source.AWS_SAM,
        },
        {
            "name": "another-secret",
            "value": "test-value-2",
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
        Secret(name="secret1", value="value1", source=Source.AWS_SAM),
        Secret(name="secret2", value="value2", source=Source.OTHER)
    ]
    
    initial_count = len(await secrets_service.list_secrets())
    assert initial_count == 0, "Secrets should be empty at start of test"
    
    for secret in secrets:
        await secrets_service.create_secret(secret)
    
    # Test listing
    result = await secrets_service.list_secrets()
    assert len(result) == len(secrets)
    assert all(isinstance(s, Secret) for s in result)

@pytest.mark.asyncio
async def test_update_secret(secrets_service):
    # Create a test secret
    secret = Secret(name="test-secret", value="test-value", source=Source.AWS_SAM)
    created_secret = await secrets_service.create_secret(secret)
    
    # Update the secret
    updated_data = Secret(
        name="updated-secret",
        value="updated-value",
        source=Source.OTHER,
        identifier=created_secret.identifier
    )
    result = await secrets_service.update_secret(created_secret.identifier, updated_data)
    
    # Verify update
    assert result is not None
    assert result.name == "updated-secret"
    assert result.source == Source.OTHER
    assert result.identifier == created_secret.identifier
    
    # Try updating non-existent secret
    non_existent = await secrets_service.update_secret("non-existent", updated_data)
    assert non_existent is None

@pytest.mark.asyncio
async def test_delete_secret(secrets_service):
    # Create a test secret
    secret = Secret(name="test-secret", value="test-value", source=Source.AWS_SAM)
    created_secret = await secrets_service.create_secret(secret)
    
    # Verify initial state
    initial_secrets = await secrets_service.list_secrets()
    assert len(initial_secrets) == 1
    
    # Delete the secret
    result = await secrets_service.delete_secret(created_secret.identifier)
    assert result is True
    
    # Verify deletion
    remaining_secrets = await secrets_service.list_secrets()
    assert len(remaining_secrets) == 0
    
    # Try deleting non-existent secret
    result = await secrets_service.delete_secret("non-existent")
    assert result is False
