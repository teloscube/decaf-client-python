__all__ = [
    "ActionResource",
    "Actions",
]

from decimal import Decimal
from typing import Any, List, Optional

from decaf.api.client.machinery import BaseResource, ResourceListEndpoint
from decaf.api.client.types import (
    GUID,
    AccountId,
    ActionId,
    ActionTypeId,
    AgentId,
    AnalyticalTypeId,
    ArtifactId,
    ArtifactTypeId,
    Currency,
    Date,
    DateTime,
    InstitutionId,
    QuantId,
    StrategyId,
    Tags,
    UserId,
    _LaterI,
)


class ActionResource(BaseResource):
    id: ActionId
    guid: GUID
    created: DateTime
    creator: Optional[UserId]
    updated: DateTime
    updater: Optional[UserId]
    ctype: ActionTypeId
    type: str
    stype: Optional[str]
    atype: Optional[AnalyticalTypeId]
    cflag: Optional[int]
    commitment: Date
    settlement: Date
    executedat: Optional[str]
    pseudorder: Optional[int]
    resmain_type: str
    resmain_ctype: ArtifactTypeId
    resmain_stype: Optional[str]
    accmain: AccountId
    accmain_guid: GUID
    accmain_name: str
    resmain: ArtifactId
    resmain_guid: GUID
    resmain_symbol: str
    qtymain: Decimal
    accaltn: Optional[AccountId]
    accaltn_guid: Optional[GUID]
    accaltn_name: Optional[str]
    resaltn: Optional[ArtifactId]
    resaltn_guid: Optional[GUID]
    resaltn_symbol: Optional[str]
    qtyaltn: Optional[Decimal]
    acccomp: Optional[AccountId]
    acccomp_guid: Optional[GUID]
    acccomp_name: Optional[str]
    rescomp: Optional[ArtifactId]
    rescomp_guid: Optional[GUID]
    rescomp_symbol: Optional[str]
    qtycomp: Optional[Decimal]
    accundr: Optional[AccountId]
    accundr_guid: Optional[GUID]
    accundr_name: Optional[str]
    resundr: Optional[ArtifactId]
    resundr_guid: Optional[GUID]
    resundr_symbol: Optional[str]
    qtyundr: Optional[Decimal]
    acccntr: Optional[AccountId]
    acccntr_guid: Optional[GUID]
    acccntr_name: Optional[str]
    rescntr: Optional[ArtifactId]
    rescntr_guid: Optional[GUID]
    rescntr_symbol: Optional[str]
    qtycntr: Optional[Decimal]
    accprin: Optional[AccountId]
    accprin_guid: Optional[GUID]
    accprin_name: Optional[str]
    resprin: Optional[ArtifactId]
    resprin_guid: Optional[GUID]
    resprin_symbol: Optional[str]
    qtyprin: Optional[Decimal]
    accintr: Optional[AccountId]
    accintr_guid: Optional[GUID]
    accintr_name: Optional[str]
    resintr: Optional[ArtifactId]
    resintr_guid: Optional[GUID]
    resintr_symbol: Optional[str]
    qtyintr: Optional[Decimal]
    pxmain: Optional[Decimal]
    pxcost: Optional[Decimal]
    pxaux1: Optional[Decimal]
    pxaux2: Optional[Decimal]
    pxaux3: Optional[Decimal]
    pxnavs: Optional[Decimal]
    shrcls: Optional[_LaterI]
    shrcls_name: Optional[str]
    shrcnt: Optional[Decimal]
    agent: Optional[AgentId]
    agent_name: Optional[str]
    feeagt: Optional[InstitutionId]
    feeagt_name: Optional[str]
    feeccy: Optional[Currency]
    feeqty: Optional[Decimal]
    reference: Optional[str]
    remapcode: Optional[str]
    notes: Optional[str]
    remarks: Optional[str]
    is_auto: bool
    is_approved: bool
    is_locked: bool
    grouping1: Optional[str]
    grouping2: Optional[str]
    grouping3: Optional[str]
    grouping4: Optional[str]
    extfld1tag: Optional[str]
    extfld1typ: Optional[str]
    extfld1val: Optional[str]
    extfld2tag: Optional[str]
    extfld2typ: Optional[str]
    extfld2val: Optional[str]
    extfld3tag: Optional[str]
    extfld3typ: Optional[str]
    extfld3val: Optional[str]
    extfld4tag: Optional[str]
    extfld4typ: Optional[str]
    extfld4val: Optional[str]
    tags: Tags
    strategy: Optional[StrategyId]
    strategy_name: Optional[str]
    auxdata: Optional[Any]
    quants: List[QuantId]


class Actions(ResourceListEndpoint[ActionResource]):
    endpoint = "trades"
    resource = ActionResource
