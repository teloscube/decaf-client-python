__all__ = [
    "QuantResource",
    "Quants",
]

from decimal import Decimal
from typing import Optional

from decaf.api.client.machinery import BaseResource, ResourceListEndpoint
from decaf.api.client.types import (
    GUID,
    AccountId,
    ActionId,
    ArtifactId,
    Currency,
    Date,
    DateTime,
    QuantId,
    UserId,
    _LaterI,
)


class QuantResource(BaseResource):
    id: QuantId
    guid: GUID
    created: DateTime
    creator: Optional[UserId] = None
    updated: DateTime
    updater: Optional[UserId] = None
    commitment: Date
    settlement: Date
    executedat: Optional[str] = None
    pseudorder: Optional[int] = None
    symbol: str
    resource: ArtifactId
    quantity: Decimal
    valccy: Currency
    valamt: Decimal
    account: AccountId
    account__name: str
    trade: ActionId
    ctype: _LaterI
    type: str
    cflag: Optional[int] = None
    refccy: Optional[Currency] = None
    refamt: Optional[Decimal] = None


class Quants(ResourceListEndpoint[QuantResource]):
    endpoint = "quants"
    resource = QuantResource
