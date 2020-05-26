__all__ = [
    "ArtifactTypeResource",
    "ArtifactTypes",
]

from typing import List, Optional

from pydantic import BaseModel, Field

from decaf.api.client.machinery import BaseResource, ResourceListEndpoint
from decaf.api.client.types import ArtifactTypeId


class ArtifactTypeField(BaseModel):
    name: str
    label: str
    auto: bool
    readonly: bool
    required: bool
    needed: bool
    help: Optional[str]


class ArtifactTypeResource(BaseResource):
    id: ArtifactTypeId
    name: str
    order: int
    fieldset: List[ArtifactTypeField] = Field(..., alias="fields")


class ArtifactTypes(ResourceListEndpoint[ArtifactTypeResource]):
    endpoint = "resources/types"
    resource = ArtifactTypeResource
