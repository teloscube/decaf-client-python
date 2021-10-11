__all__ = [
    "StockLevels",
    "StockResource",
    "Stocks",
]

import datetime
from decimal import Decimal
from enum import Enum
from typing import List, Optional

from typing_extensions import Literal

from ..machinery import BaseResource, ResourceEndpoint, query
from ..types import GUID, AccountId, ArtifactId, ArtifactTypeId, InstitutionId, PortfolioId, TeamId


class StockResource(BaseResource):
    artifact: ArtifactId
    artifact_guid: GUID
    artifact_ctype: ArtifactTypeId
    artifact_stype: Optional[str]
    artifact_symbol: str
    artifact_name: Optional[str]
    account: AccountId
    account_guid: GUID
    account_name: str
    portfolio: PortfolioId
    portfolio_guid: GUID
    portfolio_name: str
    team: TeamId
    team_guid: GUID
    team_name: str
    custodian: InstitutionId
    custodian_guid: GUID
    custodian_name: str
    quantity: Decimal


class StockLevels(Enum):
    Account = "account"
    Portfolio = "portfolio"
    Team = "team"
    Institution = "institution"


class Stocks(ResourceEndpoint[StockResource]):
    endpoint = "stocks"
    resource = StockResource

    @query
    def get(
        self,
        date: datetime.date,
        datetype: Literal["commitment", "settlement"] = "commitment",
        zero: bool = False,
        level: Optional[StockLevels] = None,
        containers: Optional[List[int]] = None,
        artifacts: Optional[List[int]] = None,
    ) -> List[StockResource]:
        """
        Attempts to get stocks.

        :param date: Date of stocks.
        :param datetype: Type of date of stocks.
        :param zero: Indicates if square positions should be reported, too.
        :param level: Container level.
        :param containers: Container ids.
        :param artifacts: Artifact its.
        :return: List of stocks.
        """
        return [
            StockResource(**i)
            for i in self.client.request(
                "GET",
                self.endpoint,
                params={
                    "date": str(date),
                    "datetype": datetype,
                    "zero": "1" if zero else "0",
                    **({} if level is None else {"c": level.value}),
                    **({} if containers is None else {"i": ",".join(map(str, containers))}),
                    **({} if artifacts is None else {"a": ",".join(map(str, artifacts))}),
                    "rich": "1",
                },
            )
        ]
