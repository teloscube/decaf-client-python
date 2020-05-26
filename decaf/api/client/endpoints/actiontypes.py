__all__ = [
    "ActionTypeResource",
    "ActionTypes",
]

from typing import List, Optional

from pydantic import BaseModel, Field

from decaf.api.client.machinery import BaseResource, ResourceListEndpoint
from decaf.api.client.types import ActionTypeId, ArtifactTypeId


class ActionTypeField(BaseModel):
    name: str
    label: str
    auto: bool
    readonly: bool
    required: bool
    needed: bool
    help: Optional[str]


class ActionTypeResource(BaseResource):
    id: ActionTypeId
    name: str
    atype: ArtifactTypeId
    fieldset: List[ActionTypeField] = Field(..., alias="fields")


class ActionTypes(ResourceListEndpoint[ActionTypeResource]):
    endpoint = "trades/types"
    resource = ActionTypeResource
