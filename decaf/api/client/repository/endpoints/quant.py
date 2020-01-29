__all__ = ["QuantResource"]

from decimal import Decimal
from typing import Optional

from decaf.api.client.repository.commons import BaseResource, Date, DateTime
from decaf.api.client.repository.types import GUID, AccountId, ActionId, ArtifactId, Currency, _LaterI


class QuantResource(BaseResource):
    id: AccountId
    guid: GUID
    created: DateTime
    creator: Optional[_LaterI]
    updated: DateTime
    updater: Optional[_LaterI]
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
