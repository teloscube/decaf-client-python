__all__ = [
    "AnalyticalTypeResource",
    "AnalyticalTypes",
]

from typing import Optional

from decaf.api.client.machinery import BaseResource, ResourceListEndpoint
from decaf.api.client.types import GUID, AnalyticalTypeId, DateTime, UserId


class AnalyticalTypeResource(BaseResource):
    id: AnalyticalTypeId
    guid: GUID
    created: DateTime
    creator: Optional[UserId] = None
    updated: DateTime
    updater: Optional[UserId] = None
    name: str
    description: Optional[str] = None


class AnalyticalTypes(ResourceListEndpoint[AnalyticalTypeResource]):
    endpoint = "analyticaltypes"
    resource = AnalyticalTypeResource
