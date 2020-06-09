__all__ = [
    "ArtifactResource",
    "Artifacts",
]

from decimal import Decimal
from typing import Any, Dict, Optional

from decaf.api.client.machinery import BaseResource, ResourceListEndpoint, ResourceRetrieveEndpoint
from decaf.api.client.types import (
    GUID,
    ArtifactId,
    ArtifactTypeId,
    AssetClassId,
    Currency,
    Date,
    DateTime,
    RiskProfileId,
    Tags,
    UserId,
    _LaterS,
)


class ArtifactResource(BaseResource):
    id: ArtifactId
    guid: GUID
    created: DateTime
    creator: Optional[UserId]
    updated: DateTime
    updater: Optional[UserId]
    incomplete: bool
    cflag: Optional[int]
    type: str
    ctype: ArtifactTypeId
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


class Artifacts(ResourceListEndpoint[ArtifactResource], ResourceRetrieveEndpoint[ArtifactId, ArtifactResource]):
    endpoint = "resources"
    resource = ArtifactResource
