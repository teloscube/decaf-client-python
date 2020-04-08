__all__ = [
    "InstitutionResource",
    "InstitutionCreateForm",
    "InstitutionUpdateForm",
    "InstitutionPatchForm",
    "Institutions",
]

from decimal import Decimal
from typing import List, Optional, Union

from decaf.api.client.machinery import (
    BaseCreateForm,
    BasePatchForm,
    BaseResource,
    BaseUpdateForm,
    Missing,
    StandardResourceEndpoint,
)
from decaf.api.client.types import GUID, AccountId, DateTime, InstitutionId, SharingId, UserId


class InstitutionResource(BaseResource):
    id: InstitutionId
    guid: GUID
    created: DateTime
    creator: Optional[UserId]
    updated: DateTime
    updater: Optional[UserId]
    name: str
    accounts: List[AccountId]
    sharings: List[SharingId]
    sharing: Optional[Decimal]
    kickback: Optional[Decimal]


class InstitutionCreateForm(BaseCreateForm):
    guid: Union[GUID, Missing] = Missing.field()
    name: str


class InstitutionUpdateForm(BaseUpdateForm):
    guid: GUID
    name: str


class InstitutionPatchForm(BasePatchForm):
    guid: Union[GUID, Missing] = Missing.field()
    name: Union[str, Missing] = Missing.field()


class Institutions(
    StandardResourceEndpoint[
        InstitutionId, InstitutionCreateForm, InstitutionUpdateForm, InstitutionPatchForm, InstitutionResource
    ]
):
    endpoint = "institutions"
    resource = InstitutionResource
