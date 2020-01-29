__all__ = [
    "BaseCreateForm",
    "BaseRepository",
    "BaseResource",
    "BasePatchForm",
    "BaseUpdateForm",
    "Date",
    "DateTime",
    "Missing",
]

from dataclasses import dataclass
from datetime import date as Date
from datetime import datetime as DateTime
from typing import Any, ClassVar, Generic, Iterable, Optional, Type, TypeVar, Union

from pydantic import BaseModel, Field

from decaf.api.client.machinery import Client, RParams


class BaseResource(BaseModel):
    """
    Provides a base class for standard DECAF resource models.
    """

    pass


class BaseCreateForm(BaseModel):
    """
    Provides a base class for standard DECAF form models for resource creation.
    """

    pass


#: Defines a type alias for resource identifiers.
_I = TypeVar("_I", bound=Union[str, int])


class BaseUpdateForm(BaseModel):
    """
    Provides a base class for standard DECAF form models for resource updation.
    """

    pass


class BasePatchForm(BaseModel):
    """
    Provides a base class for standard DECAF form models for resource patching.
    """

    class Config:
        arbitrary_types_allowed = True


class Missing:
    """
    Provides a placeholder value for missing field values.
    """

    @classmethod
    def field(cls) -> Any:
        return Field(cls())


#: Defines a type alias for :py:class:`BaseResource` implementations.
_R = TypeVar("_R", bound=BaseResource)


#: Defines a type alias for :py:class:`BaseCreateForm` implementations.
_C = TypeVar("_C", bound=BaseCreateForm)


#: Defines a type alias for :py:class:`BaseUpdateForm` implementations.
_U = TypeVar("_U", bound=BaseUpdateForm)


#: Defines a type alias for :py:class:`BasePatchForm` implementations.
_P = TypeVar("_P", bound=BasePatchForm)


@dataclass(frozen=True)
class BaseRepository(Generic[_I, _R, _C, _U, _P]):
    """
    Provides a generic resource repository implementation.
    """

    __slots__ = ["client"]

    #: Underlying client.
    client: Client

    #: Base path segment for the remote resource URI.
    endpoint: ClassVar[str]

    #: Type of the identifier of the resource.
    identifier: ClassVar[Type[_I]]

    #: Resource model of the resource.
    resource: ClassVar[Type[_R]]

    #: Create form model of the resource.
    form_create: ClassVar[Type[_C]]

    #: Update form model of the resource.
    form_update: ClassVar[Type[_U]]

    #: Patch form model of the resource.
    form_patch: ClassVar[Type[_P]]

    def list(self, params: Optional[RParams] = None) -> Iterable[_R]:
        return (
            self.resource(**d)
            for d in self.client.request("GET", self.endpoint, params={**(params or {}), "page_size": "-1"})
        )

    def get(self, ident: _I) -> _R:
        return self.resource(**self.client.request("GET", [self.endpoint, ident]))

    def create(self, form: _C) -> _R:
        return self.resource(**self.client.request("POST", self.endpoint, json=dict(form)))

    def update(self, ident: _I, form: _U) -> _R:
        return self.resource(**self.client.request("PUT", [self.endpoint, ident], json=dict(form)))

    def patch(self, ident: _I, form: _P) -> _R:
        return self.resource(
            **self.client.request(
                "PATCH", [self.endpoint, ident], json={k: v for k, v in form if not isinstance(v, Missing)}
            )
        )

    def delete(self, ident: _I) -> None:
        self.client.request("DELETE", [self.endpoint, ident])
