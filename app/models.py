from enum import Enum
from pydantic import BaseModel, Field
from ulid import ULID

class Source(str, Enum):
    AWS_SAM = "AWS_SAM"
    OTHER = "OTHER"

class Secret(BaseModel):
    name: str = Field(..., description="Name of the secret")
    source: Source = Field(..., description="Source of the secret")
    identifier: str = Field(
        default_factory=lambda: str(ULID()),
        description="ULID identifier"
    )
