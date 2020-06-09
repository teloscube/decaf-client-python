__all__ = [
    "PortfolioCreateForm",
    "PortfolioPatchForm",
    "PortfolioResource",
    "PortfolioUpdateForm",
    "Portfolios",
]

from typing import List, Optional, Union

from decaf.api.client.machinery import (
    BaseCreateForm,
    BasePatchForm,
    BaseResource,
    BaseUpdateForm,
    Missing,
    StandardResourceEndpoint,
)
from decaf.api.client.types import (
    GUID,
    AccountId,
    AccrualScheduleId,
    CountryId,
    Currency,
    Date,
    DateTime,
    OHLCId,
    PortfolioId,
    RiskProfileId,
    ShareClassId,
    TeamId,
    UserId,
)


class PortfolioResource(BaseResource):
    id: PortfolioId
    guid: GUID
    created: DateTime
    creator: Optional[UserId]
    updated: DateTime
    updater: Optional[UserId]
    name: str
    team: TeamId
    rccy: Currency
    sandbox: bool
    isin: Optional[str]
    domicile: Optional[CountryId]
    manager: Optional[str]
    objective: Optional[str]
    benchmark: Optional[OHLCId]
    riskprofile: Optional[RiskProfileId]
    data_source: Optional[str]
    team_name: str
    inception: Optional[Date]
    accounts: List[AccountId]
    shareclasses: List[ShareClassId]
    accrualschedules: List[AccrualScheduleId]


class PortfolioCreateForm(BaseCreateForm):
    guid: Union[GUID, Missing] = Missing.field()
    name: str
    team: TeamId
    rccy: Currency
    sandbox: bool
    isin: Optional[str]
    domicile: Optional[CountryId]
    manager: Optional[str]
    objective: Optional[str]
    benchmark: Optional[OHLCId]
    riskprofile: Optional[RiskProfileId]
    data_source: Optional[str]


class PortfolioUpdateForm(BaseUpdateForm):
    guid: GUID
    name: str
    team: TeamId
    rccy: Currency
    sandbox: bool
    isin: Optional[str]
    domicile: Optional[CountryId]
    manager: Optional[str]
    objective: Optional[str]
    benchmark: Optional[OHLCId]
    riskprofile: Optional[RiskProfileId]
    data_source: Optional[str]


class PortfolioPatchForm(BasePatchForm):
    guid: Union[GUID, Missing] = Missing.field()
    name: Union[str, Missing] = Missing.field()
    team: Union[TeamId, Missing] = Missing.field()
    rccy: Union[Currency, Missing] = Missing.field()
    sandbox: Union[bool, Missing] = Missing.field()
    isin: Union[Optional[str], Missing] = Missing.field()
    domicile: Union[Optional[CountryId], Missing] = Missing.field()
    manager: Union[Optional[str], Missing] = Missing.field()
    objective: Union[Optional[str], Missing] = Missing.field()
    benchmark: Union[Optional[OHLCId], Missing] = Missing.field()
    riskprofile: Union[Optional[RiskProfileId], Missing] = Missing.field()
    data_source: Union[Optional[str], Missing] = Missing.field()


class Portfolios(
    StandardResourceEndpoint[
        PortfolioId, PortfolioCreateForm, PortfolioUpdateForm, PortfolioPatchForm, PortfolioResource
    ]
):
    endpoint = "portfolios"
    resource = PortfolioResource
