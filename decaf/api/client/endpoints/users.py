__all__ = [
    "UserCreateForm",
    "UserPatchForm",
    "UserResource",
    "UserUpdateForm",
    "Users",
]

from typing import List, Optional, Union

from decaf.api.client.machinery import (
    BaseCreateForm,
    BasePatchForm,
    BaseResource,
    BaseUpdateForm,
    Missing,
    StandardResourceEndpoint,
    command,
)
from decaf.api.client.types import GUID, DateTime, GroupId, PortfolioGroupId, TeamId, UserId


class UserResource(BaseResource):
    id: UserId
    guid: GUID
    created: DateTime
    creator: Optional[UserId]
    updated: DateTime
    updater: Optional[UserId]
    username: str
    is_active: bool
    privileged: bool
    date_joined: DateTime
    email: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    mobile: Optional[str]
    last_login: Optional[DateTime]
    groups: List[GroupId]
    teams: List[TeamId]
    portfolio_groups: List[PortfolioGroupId]


class UserCreateForm(BaseCreateForm):
    guid: Union[GUID, Missing] = Missing.field()
    username: str
    is_active: bool
    email: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    mobile: Optional[str]
    groups: List[GroupId]
    teams: List[TeamId]


class UserUpdateForm(BaseUpdateForm):
    guid: GUID
    username: str
    is_active: bool
    email: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    mobile: Optional[str]
    groups: List[GroupId]
    teams: List[TeamId]


class UserPatchForm(BasePatchForm):
    guid: Union[GUID, Missing] = Missing.field()
    username: Union[str, Missing] = Missing.field()
    is_active: Union[bool, Missing] = Missing.field()
    email: Union[Optional[str], Missing] = Missing.field()
    first_name: Union[Optional[str], Missing] = Missing.field()
    last_name: Union[Optional[str], Missing] = Missing.field()
    mobile: Union[Optional[str], Missing] = Missing.field()
    groups: Union[List[GroupId], Missing] = Missing.field()
    teams: Union[List[TeamId], Missing] = Missing.field()


class Users(StandardResourceEndpoint[UserId, UserCreateForm, UserUpdateForm, UserPatchForm, UserResource]):
    endpoint = "users"
    resource = UserResource

    @command
    def password(self, ident: UserId, secret: str) -> None:
        """
        Attempts to set the password for the user identified by the given user.

        :param ident: User identifier.
        :param secret: New password.
        :raises APIClientError: In case that there is a problem with client-server communication.
        :raises APIServerError: In case that there is a server generated error reported via HTTP status codes.
        """
        self.client.request("POST", [self.endpoint, ident, "password"], json={"password1": secret, "password2": secret})
