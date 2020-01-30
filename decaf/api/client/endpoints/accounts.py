__all__ = [
    "AccountCreateForm",
    "AccountPatchForm",
    "AccountResource",
    "AccountUpdateForm",
    "Accounts",
]

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

from decaf.api.client.machinery import (
    BaseCreateForm,
    BasePatchForm,
    BaseResource,
    BaseUpdateForm,
    Missing,
    StandardResourceEndpoint,
    command,
    query,
)
from decaf.api.client.types import (
    GUID,
    AccountId,
    AccountMngtFeeSchemeId,
    AnalyticalTypeId,
    Currency,
    Date,
    DateTime,
    InstitutionId,
    PortfolioId,
    RiskProfileId,
    UserId,
)


class AccountResource(BaseResource):
    id: AccountId
    guid: GUID
    created: DateTime
    creator: Optional[UserId]
    updated: DateTime
    updater: Optional[UserId]
    name: str
    opened: Optional[Date]
    rccy: Currency
    portfolio: PortfolioId
    custodian: InstitutionId
    atype: Optional[AnalyticalTypeId]
    riskprofile: Optional[RiskProfileId]
    horizontype: Optional[str]
    mandatetype: Optional[str]
    data_source: Optional[str]
    htype: str
    inception: Optional[Date]
    closed: Optional[Date]
    is_active: bool
    is_closed: bool
    mfpercentage: Optional[AccountMngtFeeSchemeId]
    mfpercentages: List[AccountMngtFeeSchemeId]
    riskprofile_name: Optional[str]
    custodian_name: Optional[str]
    portfolio_name: Optional[str]
    team_name: Optional[str]


class AccountCreateForm(BaseCreateForm):
    guid: Union[GUID, Missing] = Missing.field()
    name: str
    opened: Optional[Date]
    rccy: Currency
    portfolio: PortfolioId
    custodian: InstitutionId
    atype: Optional[AnalyticalTypeId]
    riskprofile: Optional[RiskProfileId]
    horizontype: Optional[str]
    mandatetype: Optional[str]
    data_source: Optional[str]


class AccountUpdateForm(BaseUpdateForm):
    guid: GUID
    name: str
    opened: Optional[Date]
    rccy: Currency
    portfolio: PortfolioId
    custodian: InstitutionId
    atype: Optional[AnalyticalTypeId]
    riskprofile: Optional[RiskProfileId]
    horizontype: Optional[str]
    mandatetype: Optional[str]
    data_source: Optional[str]


class AccountPatchForm(BasePatchForm):
    guid: Union[GUID, Missing] = Missing.field()
    name: Union[str, Missing] = Missing.field()
    opened: Union[Optional[Date], Missing] = Missing.field()
    rccy: Union[Currency, Missing] = Missing.field()
    portfolio: Union[PortfolioId, Missing] = Missing.field()
    custodian: Union[InstitutionId, Missing] = Missing.field()
    atype: Union[Optional[AnalyticalTypeId], Missing] = Missing.field()
    riskprofile: Union[Optional[RiskProfileId], Missing] = Missing.field()
    horizontype: Union[Optional[str], Missing] = Missing.field()
    mandatetype: Union[Optional[str], Missing] = Missing.field()
    data_source: Union[Optional[str], Missing] = Missing.field()


@dataclass(frozen=True)
class AccountUpdate:
    """
    Provides a data update value model.
    """

    #: Last transaction update.
    tx: Optional[Dict[str, Any]]

    #: Last price update.
    px: Optional[Dict[str, Any]]


class Accounts(
    StandardResourceEndpoint[AccountId, AccountCreateForm, AccountUpdateForm, AccountPatchForm, AccountResource]
):
    endpoint = "accounts"
    resource = AccountResource

    @command
    def flush(self, ident: AccountId) -> None:
        """
        Attempts to purge all trades and transactions of the account (therefore related accounts, too).

        :param ident: Account identifier.
        :raises APIClientError: In case that there is a problem with client-server communication.
        :raises APIServerError: In case that there is a server generated error reported via HTTP status codes.
        """
        self.client.request("POST", [self.endpoint, ident, "flush"])

    @command
    def close(self, ident: AccountId, date: Date) -> None:
        """
        Attempts to close the account.

        :param ident: Account identifier.
        :param date: Date to close the account as of.
        :raises APIClientError: In case that there is a problem with client-server communication.
        :raises APIServerError: In case that there is a server generated error reported via HTTP status codes.
        """
        self.client.request("POST", [self.endpoint, ident, "close"], params={"asof": str(date)})

    @command
    def transfer(self, ident: AccountId, to: AccountId, date: Date) -> None:
        """
        Attempts to transfer the account to another one.

        :param ident: Identifier of the account to transfer from.
        :param to: Identifier of the account to transfer to.
        :param date: Date to close the account as of.
        :raises APIClientError: In case that there is a problem with client-server communication.
        :raises APIServerError: In case that there is a server generated error reported via HTTP status codes.
        """
        self.client.request("POST", [self.endpoint, ident, "transfer"], params={"account": str(to), "asof": str(date)})

    @query
    def updates(self, ident: AccountId) -> AccountUpdate:
        """
        Attempts to retrieve last account update information.

        :param ident: Account identifier.
        :raises APIClientError: In case that there is a problem with client-server communication.
        :raises APIServerError: In case that there is a server generated error reported via HTTP status codes.
        """
        return AccountUpdate(**self.client.request("GET", [self.endpoint, ident, "updates"]))

    @query
    def mandatetypes(self) -> List[str]:
        """
        Attempts to retrieve available mandate types.

        :raises APIClientError: In case that there is a problem with client-server communication.
        :raises APIServerError: In case that there is a server generated error reported via HTTP status codes.
        """
        return self.client.request("GET", [self.endpoint, "mandatetypes"])  # type: ignore

    @query
    def horizontypes(self) -> List[str]:
        """
        Attempts to retrieve available horizon types.

        :raises APIClientError: In case that there is a problem with client-server communication.
        :raises APIServerError: In case that there is a server generated error reported via HTTP status codes.
        """
        return self.client.request("GET", [self.endpoint, "horizontypes"])  # type: ignore
