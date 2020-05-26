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
    creator: Optional[UserId]
    updated: DateTime
    updater: Optional[UserId]
    commitment: Date
    settlement: Date
    executedat: Optional[str]
    pseudorder: Optional[int]
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
    cflag: Optional[int]
    refccy: Optional[Currency]
    refamt: Optional[Decimal]


class Quants(ResourceListEndpoint[QuantResource]):
    endpoint = "quants"
    resource = QuantResource
