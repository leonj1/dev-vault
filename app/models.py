from enum import Enum
from typing import List
from pydantic import BaseModel, Field
from ulid import ULID

class Project(BaseModel):
    name: str = Field(..., description="Name of the project")
    secrets: List[str] = Field(default_factory=list, description="List of secret identifiers")
    identifier: str = Field(
        default_factory=lambda: str(ULID()),
        description="ULID identifier"
    )

class Source(str, Enum):
    AWS_SAM = "AWS_SAM"
    OTHER = "OTHER"

class Secret(BaseModel):
    name: str = Field(..., description="Name of the secret")
    value: str = Field(..., description="Value of the secret")
    source: Source = Field(..., description="Source of the secret")
    identifier: str = Field(
        default_factory=lambda: str(ULID()),
        description="ULID identifier"
    )
