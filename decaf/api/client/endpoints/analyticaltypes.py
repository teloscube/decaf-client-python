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
    creator: Optional[UserId]
    updated: DateTime
    updater: Optional[UserId]
    name: str
    description: Optional[str]


class AnalyticalTypes(ResourceListEndpoint[AnalyticalTypeResource]):
    endpoint = "analyticaltypes"
    resource = AnalyticalTypeResource
