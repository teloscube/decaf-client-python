__all__ = [
    "ConsolidationResource",
    "Consolidation",
]

from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Iterable, List, Optional

from pydantic.main import BaseModel

from ..machinery import BaseResource, ResourceEndpoint, query
from ..types import GUID, AccountId, ArtifactId, ArtifactType, ContainerType, Currency, Date, DateTime, DateType


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


class ConsolidationAccounts(BaseModel):
    custody: List[ConsolidationAccount]
    journal: List[ConsolidationAccount]


class HoldingArtifactType(BaseModel):
    id: ArtifactType
    name: str
    order: int


class HoldingArtifact(BaseModel):
    id: ArtifactId
    guid: GUID
    type: HoldingArtifactType
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


class HoldingTagsClassificationNode(BaseModel):
    name: str
    order: str


class HoldingTags(BaseModel):
    classification: List[HoldingTagsClassificationNode]


class HoldingValuePair(BaseModel):
    org: Optional[Decimal]
    ref: Optional[Decimal]


class HoldingInvestment(BaseModel):
    px: HoldingValuePair
    txncosts: HoldingValuePair
    accrued: HoldingValuePair
    value: HoldingValuePair


class HoldingValuePairAbsNet(BaseModel):
    net: HoldingValuePair
    abs: HoldingValuePair


class HoldingValuation(BaseModel):
    px: HoldingValuePair
    accrued: HoldingValuePair
    value: HoldingValuePairAbsNet
    exposure: HoldingValuePairAbsNet


class SubHolding(BaseModel):
    artifact: HoldingArtifact
    quantity: Decimal
    accounts: List[ConsolidationAccount]
    investment: HoldingInvestment
    valuation: HoldingValuation
    change: Optional[Decimal]
    pnl: Optional[Decimal]
    pnl_to_investment: Optional[Decimal]
    opendate: Date
    lastdate: Date

    @property
    def account(self) -> ConsolidationAccount:
        return self.accounts[0]


class Holding(BaseModel):
    artifact: HoldingArtifact
    tags: HoldingTags
    quantity: Decimal
    accounts: List[ConsolidationAccount]
    investment: HoldingInvestment
    valuation: HoldingValuation
    children: List[SubHolding]
    change: Optional[Decimal]
    pnl: Optional[Decimal]
    pnl_to_investment: Optional[Decimal]
    opendate: Date
    lastdate: Date


class FXRate(BaseModel):
    ccy1: Currency
    ccy2: Currency
    value: Decimal
    asof: Date


@dataclass
class AccountHolding:
    account: ConsolidationAccount
    artifact: HoldingArtifact
    quantity: Decimal
    investment: HoldingInvestment
    valuation: HoldingValuation
    opendate: Date
    lastdate: Date
    tags: HoldingTags
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
    holdings: List[Holding]
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
    fxrates: List[FXRate]

    def get_account_level_holdings(self) -> Iterable[AccountHolding]:
        """
        Compiles account level holdings.
        """
        for topholding in self.holdings:
            if len(topholding.children) == 0:
                yield AccountHolding(
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
                    yield AccountHolding(
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
                "GET", self.endpoint, params={"datetype": dtype.value, "date": str(date), "ccy": currency},
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
