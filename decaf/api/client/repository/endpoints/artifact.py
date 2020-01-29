__all__ = ["ArtifactResource"]

from decimal import Decimal
from typing import Any, Dict, Optional

from decaf.api.client.repository.commons import BaseResource, Date, DateTime
from decaf.api.client.repository.types import (
    GUID,
    AccountId,
    ArtifactId,
    AssetClassId,
    Currency,
    RiskProfileId,
    Tags,
    _LaterI,
    _LaterS,
)


class ArtifactResource(BaseResource):
    id: AccountId
    guid: GUID
    created: DateTime
    creator: Optional[_LaterI]
    updated: DateTime
    updater: Optional[_LaterI]
    incomplete: bool
    cflag: Optional[int]
    type: str
    ctype: _LaterS
    stype: Optional[str]
    symbol: str
    name: str
    ccymain: Optional[Currency]
    ccyaltn: Optional[Currency]
    ccystlm: Optional[Currency]
    pxmain: Optional[Decimal]
    pxaltn: Optional[Decimal]
    pxflip: Optional[bool]
    pxcnst: Optional[Decimal]
    issued: Optional[Date]
    launch: Optional[Date]
    ceased: Optional[Date]
    expiry: Optional[Date]
    last_tradable: Optional[Date]
    first_notice: Optional[Date]
    horizon: Optional[Date]
    convday: Optional[_LaterS]
    underlying: Optional[ArtifactId]
    quantity: Optional[Decimal]
    lvrgfact: Optional[Decimal]
    style: Optional[str]
    callput: Optional[bool]
    frequency: Optional[int]
    eom: Optional[int]
    mic: Optional[str]
    ticker: Optional[str]
    isin: Optional[str]
    cusip: Optional[str]
    figi: Optional[str]
    telekurs: Optional[str]
    ohlccode: Optional[str]
    country: Optional[str]
    sector: Optional[str]
    sector_gics: Optional[str]
    issuer: Optional[str]
    domicile: Optional[str]
    reference: Optional[str]
    remapcode: Optional[str]
    sp_rating: Optional[str]
    sp_outlook: Optional[str]
    riskprofile: Optional[RiskProfileId]
    assetclass: Optional[AssetClassId]
    extdata: Optional[Any]
    auxdata: Optional[Any]
    description: Optional[str]
    tags: Tags
    attributes: Dict[str, Any]
