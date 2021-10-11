__all__ = [
    "Consolidation",
    "ConsolidationAccount",
    "ConsolidationAccountHolding",
    "ConsolidationAccounts",
    "ConsolidationContainer",
    "ConsolidationContainers",
    "ConsolidationFXRate",
    "ConsolidationHolding",
    "ConsolidationHoldingArtifact",
    "ConsolidationHoldingArtifactType",
    "ConsolidationHoldingInvestment",
    "ConsolidationHoldingTags",
    "ConsolidationHoldingTagsClassificationNode",
    "ConsolidationHoldingValuation",
    "ConsolidationHoldingValuePair",
    "ConsolidationHoldingValuePairAbsNet",
    "ConsolidationResource",
    "ConsolidationSubHolding",
]

from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Iterable, List, Optional

from pydantic.main import BaseModel

from ..machinery import BaseResource, ResourceEndpoint, query
from ..types import GUID, AccountId, ArtifactId, ArtifactTypeId, ContainerType, Currency, Date, DateTime, DateType


class ConsolidationContainer(BaseModel):
    id: int
    guid: GUID
    name: str


class ConsolidationContainers(BaseModel):
    level: ContainerType
    containers: List[ConsolidationContainer]


class ConsolidationAccount(BaseModel):
    id: AccountId
    guid: GUID
    name: str

    def __lt__(self, other: "ConsolidationAccount") -> bool:
        return self.name < other.name


class ConsolidationAccounts(BaseModel):
    custody: List[ConsolidationAccount]
    journal: List[ConsolidationAccount]


class ConsolidationHoldingArtifactType(BaseModel):
    id: ArtifactTypeId
    name: str
    order: int


class ConsolidationHoldingArtifact(BaseModel):
    id: ArtifactId
    guid: GUID
    type: ConsolidationHoldingArtifactType
    stype: Optional[str]
    symbol: str
    name: Optional[str]
    ccy: Optional[Currency]
    quantity: Optional[Decimal]
    country: Optional[str]
    issuer: Optional[str]
    sector: Optional[str]
    mic: Optional[str]
    ticker: Optional[str]
    isin: Optional[str]
    figi: Optional[str]
    expiry: Optional[Date]
    underlying_id: Optional[ArtifactId]

    def __lt__(self, other: "ConsolidationHoldingArtifact") -> bool:
        return self.symbol < other.symbol


class ConsolidationHoldingTagsClassificationNode(BaseModel):
    name: str
    order: str


class ConsolidationHoldingTags(BaseModel):
    classification: List[ConsolidationHoldingTagsClassificationNode]


class ConsolidationHoldingValuePair(BaseModel):
    org: Optional[Decimal]
    ref: Optional[Decimal]


class ConsolidationHoldingInvestment(BaseModel):
    px: ConsolidationHoldingValuePair
    txncosts: ConsolidationHoldingValuePair
    accrued: ConsolidationHoldingValuePair
    value: ConsolidationHoldingValuePair


class ConsolidationHoldingValuePairAbsNet(BaseModel):
    net: ConsolidationHoldingValuePair
    abs: ConsolidationHoldingValuePair


class ConsolidationHoldingValuation(BaseModel):
    px: ConsolidationHoldingValuePair
    accrued: ConsolidationHoldingValuePair
    value: ConsolidationHoldingValuePairAbsNet
    exposure: ConsolidationHoldingValuePairAbsNet


class ConsolidationSubHolding(BaseModel):
    artifact: ConsolidationHoldingArtifact
    quantity: Decimal
    accounts: List[ConsolidationAccount]
    investment: ConsolidationHoldingInvestment
    valuation: ConsolidationHoldingValuation
    change: Optional[Decimal]
    pnl: Optional[Decimal]
    pnl_to_investment: Optional[Decimal]
    opendate: Date
    lastdate: Date

    @property
    def account(self) -> ConsolidationAccount:
        return self.accounts[0]


class ConsolidationHolding(BaseModel):
    artifact: ConsolidationHoldingArtifact
    tags: ConsolidationHoldingTags
    quantity: Decimal
    accounts: List[ConsolidationAccount]
    investment: ConsolidationHoldingInvestment
    valuation: ConsolidationHoldingValuation
    children: List[ConsolidationSubHolding]
    change: Optional[Decimal]
    pnl: Optional[Decimal]
    pnl_to_investment: Optional[Decimal]
    opendate: Date
    lastdate: Date


class ConsolidationFXRate(BaseModel):
    ccy1: Currency
    ccy2: Currency
    value: Decimal
    asof: Date


@dataclass
class ConsolidationAccountHolding:
    account: ConsolidationAccount
    artifact: ConsolidationHoldingArtifact
    quantity: Decimal
    investment: ConsolidationHoldingInvestment
    valuation: ConsolidationHoldingValuation
    opendate: Date
    lastdate: Date
    tags: ConsolidationHoldingTags
    change: Optional[Decimal]
    pnl: Optional[Decimal]
    pnl_to_investment: Optional[Decimal]


class ConsolidationResource(BaseResource):
    reported: DateTime
    asof: Date
    type: "DateType"
    ccy: Currency
    containers: ConsolidationContainers
    accounts: ConsolidationAccounts
    holdings: List[ConsolidationHolding]
    accruals: List[Any]  # TODO: Complete
    investment: Optional[Decimal]
    valuation_net: Optional[Decimal]
    valuation_abs: Optional[Decimal]
    accrued: Optional[Decimal]
    liabilities: Optional[Decimal]
    gav: Optional[Decimal]
    nav: Decimal
    aum: Decimal
    pnl: Decimal
    pnl_to_investment: Optional[Decimal]
    fxrates: List[ConsolidationFXRate]

    def get_account_level_holdings(self) -> Iterable[ConsolidationAccountHolding]:
        """
        Compiles account level holdings.
        """
        for topholding in self.holdings:
            if len(topholding.children) == 0:
                yield ConsolidationAccountHolding(
                    account=topholding.accounts[0],
                    artifact=topholding.artifact,
                    quantity=topholding.quantity,
                    investment=topholding.investment,
                    valuation=topholding.valuation,
                    opendate=topholding.opendate,
                    lastdate=topholding.lastdate,
                    tags=topholding.tags,
                    change=topholding.change,
                    pnl=topholding.pnl,
                    pnl_to_investment=topholding.pnl_to_investment,
                )
            else:
                for subholding in topholding.children:
                    yield ConsolidationAccountHolding(
                        account=subholding.accounts[0],
                        artifact=subholding.artifact,
                        quantity=subholding.quantity,
                        investment=subholding.investment,
                        valuation=subholding.valuation,
                        opendate=subholding.opendate,
                        lastdate=subholding.lastdate,
                        tags=topholding.tags,
                        change=subholding.change,
                        pnl=subholding.pnl,
                        pnl_to_investment=topholding.pnl_to_investment,
                    )


class Consolidation(ResourceEndpoint[ConsolidationResource]):
    endpoint = "consolidation"
    resource = ConsolidationResource

    @query
    def all(self, dtype: DateType, date: Date, currency: Currency) -> ConsolidationResource:
        """
        Attempts to get the consolidation for all containers at once.

        :param dtype: Date type.
        :param date: Date of consolidation.
        :param currency: Reference currency.
        :raises APIClientError: In case that there is a problem with client-server communication.
        :raises APIServerError: In case that there is a server generated error reported via HTTP status codes.
        """
        return ConsolidationResource(
            **self.client.request(
                "GET",
                self.endpoint,
                params={"datetype": dtype.value, "date": str(date), "ccy": currency},
            )
        )

    @query
    def get(
        self, ctype: ContainerType, containers: List[int], dtype: DateType, date: Date, currency: Currency
    ) -> ConsolidationResource:
        """
        Attempts to get the consolidation for the query.

        :param ctype: Container type.
        :param containers: Container identifiers.
        :param dtype: Date type.
        :param date: Date of consolidation.
        :param currency: Reference currency.
        :raises APIClientError: In case that there is a problem with client-server communication.
        :raises APIServerError: In case that there is a server generated error reported via HTTP status codes.
        """
        return ConsolidationResource(
            **self.client.request(
                "GET",
                self.endpoint,
                params={"c": ctype.value, "i": containers, "datetype": dtype.value, "date": str(date), "ccy": currency},
            )
        )
