__all__ = [
    "TeamCreateForm",
    "TeamPatchForm",
    "TeamResource",
    "TeamUpdateForm",
    "Teams",
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
from decaf.api.client.types import GUID, DateTime, PortfolioId, TeamId, UserId


class TeamResource(BaseResource):
    id: TeamId
    guid: GUID
    created: DateTime
    creator: Optional[UserId]
    updated: DateTime
    updater: Optional[UserId]
    name: str
    members: List[UserId]
    portfolios: List[PortfolioId]


class TeamCreateForm(BaseCreateForm):
    guid: Union[GUID, Missing] = Missing.field()
    name: str
    members: List[UserId]


class TeamUpdateForm(BaseUpdateForm):
    guid: GUID
    name: str
    members: List[UserId]


class TeamPatchForm(BasePatchForm):
    guid: Union[GUID, Missing] = Missing.field()
    name: Union[str, Missing] = Missing.field()
    members: Union[str, List[UserId]] = Missing.field()


class Teams(StandardResourceEndpoint[TeamId, TeamCreateForm, TeamUpdateForm, TeamPatchForm, TeamResource]):
    endpoint = "teams"
    resource = TeamResource
