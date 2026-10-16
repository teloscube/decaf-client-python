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
    creator: Optional[UserId] = None
    updated: DateTime
    updater: Optional[UserId] = None
    ctype: ActionTypeId
    type: str
    stype: Optional[str] = None
    atype: Optional[AnalyticalTypeId] = None
    cflag: Optional[int] = None
    commitment: Date
    settlement: Date
    executedat: Optional[str] = None
    pseudorder: Optional[int] = None
    resmain_type: str
    resmain_ctype: ArtifactTypeId
    resmain_stype: Optional[str] = None
    accmain: AccountId
    accmain_guid: GUID
    accmain_name: str
    resmain: ArtifactId
    resmain_guid: GUID
    resmain_symbol: str
    qtymain: Decimal
    accaltn: Optional[AccountId] = None
    accaltn_guid: Optional[GUID] = None
    accaltn_name: Optional[str] = None
    resaltn: Optional[ArtifactId] = None
    resaltn_guid: Optional[GUID] = None
    resaltn_symbol: Optional[str] = None
    qtyaltn: Optional[Decimal] = None
    acccomp: Optional[AccountId] = None
    acccomp_guid: Optional[GUID] = None
    acccomp_name: Optional[str] = None
    rescomp: Optional[ArtifactId] = None
    rescomp_guid: Optional[GUID] = None
    rescomp_symbol: Optional[str] = None
    qtycomp: Optional[Decimal] = None
    accundr: Optional[AccountId] = None
    accundr_guid: Optional[GUID] = None
    accundr_name: Optional[str] = None
    resundr: Optional[ArtifactId] = None
    resundr_guid: Optional[GUID] = None
    resundr_symbol: Optional[str] = None
    qtyundr: Optional[Decimal] = None
    acccntr: Optional[AccountId] = None
    acccntr_guid: Optional[GUID] = None
    acccntr_name: Optional[str] = None
    rescntr: Optional[ArtifactId] = None
    rescntr_guid: Optional[GUID] = None
    rescntr_symbol: Optional[str] = None
    qtycntr: Optional[Decimal] = None
    accprin: Optional[AccountId] = None
    accprin_guid: Optional[GUID] = None
    accprin_name: Optional[str] = None
    resprin: Optional[ArtifactId] = None
    resprin_guid: Optional[GUID] = None
    resprin_symbol: Optional[str] = None
    qtyprin: Optional[Decimal] = None
    accintr: Optional[AccountId] = None
    accintr_guid: Optional[GUID] = None
    accintr_name: Optional[str] = None
    resintr: Optional[ArtifactId] = None
    resintr_guid: Optional[GUID] = None
    resintr_symbol: Optional[str] = None
    qtyintr: Optional[Decimal] = None
    pxmain: Optional[Decimal] = None
    pxcost: Optional[Decimal] = None
    pxaux1: Optional[Decimal] = None
    pxaux2: Optional[Decimal] = None
    pxaux3: Optional[Decimal] = None
    pxnavs: Optional[Decimal] = None
    shrcls: Optional[_LaterI] = None
    shrcls_name: Optional[str] = None
    shrcnt: Optional[Decimal] = None
    agent: Optional[AgentId] = None
    agent_name: Optional[str] = None
    feeagt: Optional[InstitutionId] = None
    feeagt_name: Optional[str] = None
    feeccy: Optional[Currency] = None
    feeqty: Optional[Decimal] = None
    reference: Optional[str] = None
    remapcode: Optional[str] = None
    notes: Optional[str] = None
    remarks: Optional[str] = None
    is_auto: bool
    is_approved: bool
    is_locked: bool
    grouping1: Optional[str] = None
    grouping2: Optional[str] = None
    grouping3: Optional[str] = None
    grouping4: Optional[str] = None
    extfld1tag: Optional[str] = None
    extfld1typ: Optional[str] = None
    extfld1val: Optional[str] = None
    extfld2tag: Optional[str] = None
    extfld2typ: Optional[str] = None
    extfld2val: Optional[str] = None
    extfld3tag: Optional[str] = None
    extfld3typ: Optional[str] = None
    extfld3val: Optional[str] = None
    extfld4tag: Optional[str] = None
    extfld4typ: Optional[str] = None
    extfld4val: Optional[str] = None
    tags: Tags
    strategy: Optional[StrategyId] = None
    strategy_name: Optional[str] = None
    auxdata: Optional[Any] = None
    quants: List[QuantId]


class Actions(ResourceListEndpoint[ActionResource]):
    endpoint = "trades"
    resource = ActionResource
