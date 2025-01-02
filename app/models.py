from enum import Enum
from typing import List, ForwardRef
from pydantic import BaseModel, Field
from ulid import ULID

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

class Project(BaseModel):
    name: str = Field(..., description="Name of the project")
    secrets: List[Secret] = Field(default_factory=list, description="List of secrets")
    identifier: str = Field(
        default_factory=lambda: str(ULID()),
        description="ULID identifier"
    )
