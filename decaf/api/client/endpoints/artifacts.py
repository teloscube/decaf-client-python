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
    creator: Optional[UserId] = None
    updated: DateTime
    updater: Optional[UserId] = None
    incomplete: bool
    cflag: Optional[int] = None
    type: str
    ctype: ArtifactTypeId
    stype: Optional[str] = None
    symbol: str
    name: str
    ccymain: Optional[Currency] = None
    ccyaltn: Optional[Currency] = None
    ccystlm: Optional[Currency] = None
    pxmain: Optional[Decimal] = None
    pxaltn: Optional[Decimal] = None
    pxflip: Optional[bool] = None
    pxcnst: Optional[Decimal] = None
    issued: Optional[Date] = None
    launch: Optional[Date] = None
    ceased: Optional[Date] = None
    expiry: Optional[Date] = None
    last_tradable: Optional[Date] = None
    first_notice: Optional[Date] = None
    horizon: Optional[Date] = None
    convday: Optional[_LaterS] = None
    underlying: Optional[ArtifactId] = None
    quantity: Optional[Decimal] = None
    lvrgfact: Optional[Decimal] = None
    style: Optional[str] = None
    callput: Optional[bool] = None
    frequency: Optional[int] = None
    eom: Optional[int] = None
    mic: Optional[str] = None
    ticker: Optional[str] = None
    isin: Optional[str] = None
    cusip: Optional[str] = None
    figi: Optional[str] = None
    telekurs: Optional[str] = None
    ohlccode: Optional[str] = None
    country: Optional[str] = None
    sector: Optional[str] = None
    sector_gics: Optional[str] = None
    issuer: Optional[str] = None
    domicile: Optional[str] = None
    reference: Optional[str] = None
    remapcode: Optional[str] = None
    sp_rating: Optional[str] = None
    sp_outlook: Optional[str] = None
    riskprofile: Optional[RiskProfileId] = None
    assetclass: Optional[AssetClassId] = None
    extdata: Optional[Any] = None
    auxdata: Optional[Any] = None
    description: Optional[str] = None
    tags: Tags
    attributes: Dict[str, Any]


class Artifacts(ResourceListEndpoint[ArtifactResource], ResourceRetrieveEndpoint[ArtifactId, ArtifactResource]):
    endpoint = "resources"
    resource = ArtifactResource
