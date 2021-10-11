"""
This module provides the essential machinery to perform remote API requests and define endpoint client implementations.
"""

__all__ = [
    "APIClientError",
    "APIHeaderAuthorization",
    "APIKeyAuthorization",
    "APIServerError",
    "APIServerErrorBadAuthorization",
    "APIServerErrorBadRequest",
    "APIServerErrorBlowup",
    "APIServerErrorNotFound",
    "APITokenAuthorization",
    "Authorization",
    "BaseCreateForm",
    "BasePatchForm",
    "BaseResource",
    "BaseUpdateForm",
    "Client",
    "DeleteEndpoint",
    "Endpoint",
    "Error",
    "Missing",
    "RFiles",
    "RHeaders",
    "RMethod",
    "RParams",
    "RPath",
    "RTimeout",
    "Request",
    "ResourceCreateEndpoint",
    "ResourceEndpoint",
    "ResourceListEndpoint",
    "ResourcePatchEndpoint",
    "ResourceRetrieveEndpoint",
    "ResourceUpdateEndpoint",
    "StandardResourceEndpoint",
    "command",
    "query",
]

import re
import time
from abc import abstractmethod
from dataclasses import dataclass, field
from json import load as loadjson
from pathlib import Path
from typing import (
    Any,
    BinaryIO,
    Callable,
    ClassVar,
    Dict,
    Generator,
    Generic,
    Iterable,
    List,
    Optional,
    Set,
    TextIO,
    Tuple,
    Type,
    TypeVar,
    Union,
)
from urllib.parse import urljoin

import requests
from pydantic import BaseModel, Field
from requests.auth import AuthBase
from typing_extensions import Literal


@dataclass(frozen=True)
class Error(Exception):
    """
    Provides a base exception model for the DECAF client library.

    .. note:: You should probably catch sub-classes of this exception class.
    """

    #: Error message.
    message: str


@dataclass(frozen=True)
class APIClientError(Error):
    """
    Provides an exception model for errors generated during request-response cycle (not by the API server).
    """

    #: Underlying exception.
    underlying: Exception


@dataclass(frozen=True)
class APIServerError(Error):
    """
    Provides an exception for API server generated errors.
    """

    #: HTTP status code of the error response received from the API server.
    status: int

    #: Payload of the error response received from the API server.
    payload: Union[str, bytes, None]


@dataclass(frozen=True)
class APIServerErrorBadRequest(APIServerError):
    """
    Provides an exception for API server generated HTTP 400 errors.
    """

    #: Error definition.
    feedback: Dict[str, List[str]]


@dataclass(frozen=True)
class APIServerErrorBadAuthorization(APIServerError):
    """
    Provides an exception for API server generated HTTP 401, 403 and 405 errors.
    """

    pass


@dataclass(frozen=True)
class APIServerErrorNotFound(APIServerError):
    """
    Provides an exception for API server generated HTTP 404 errors.
    """

    pass


@dataclass(frozen=True)
class APIServerErrorBlowup(APIServerError):
    """
    Provides an exception for API server generated HTTP 5XX errors.
    """

    pass


#: Defines a type alias for HTTP verbs.
RMethod = Literal["GET", "POST", "PUT", "PATCH", "DELETE"]

#: Defines a type alias for relative path or path segments of the remote API endpoint.
RPath = Union[str, List[Union[str, int]]]

#: Defines a type alias for query-string parameters.
RParams = Dict[str, Union[str, int, List[str], List[int]]]

#: Defines a type alias for HTTP request headers.
RHeaders = Dict[str, str]

#: Defines a type alias for file objects.
_FileObject = Union[str, bytes, bytearray, TextIO, BinaryIO]

#: Defines a type alias for file object maps to be passed for multi-part uploads.
RFiles = Dict[str, Union[_FileObject, Tuple[_FileObject, str], Tuple[_FileObject, str, Dict[str, str]]]]

#: Defines a type alias for HTTP request timeouts.
RTimeout = Tuple[float, float]


@dataclass(frozen=True)
class Request:
    """
    Defines a high(ish)-level client request model.
    """

    #: Request method.
    method: RMethod

    #: Relative path or path segments for the remote API endpoint URL.
    path: RPath

    #: Request parameters, if any.
    params: Optional[RParams] = None

    #: Request data payload, if any.
    data: Any = None

    #: Request data payload in JSON, if any (convenience for sending ``application/json`` payloads).
    json: Any = None

    #: Request data payload files, if any (convenience for uploading multipart payloads).
    files: Optional[RFiles] = None

    #: Request headers.
    headers: Optional[RHeaders] = None

    #: Defines the timeout, if any:
    timeout: Optional[RTimeout] = None


class Authorization:
    """
    Provides a base class for client authorization.
    """

    @abstractmethod
    def headers(self) -> Dict[str, str]:
        """
        Provides the client authorization header for HTTP requests.
        """
        pass


@dataclass(frozen=True)
class APIKeyAuthorization(Authorization):
    """
    Provides API key authorization method.
    """

    #: Defines the API key.
    key: str = field(repr=False)

    #: Defines the API secret.
    scr: str = field(repr=False)

    def headers(self) -> Dict[str, str]:
        return {"Authorization": f"Key {self.key}:{self.scr}"}


@dataclass(frozen=True)
class APITokenAuthorization(Authorization):
    """
    Provides API token authorization method.
    """

    #: API token.
    token: str = field(repr=False)

    def headers(self) -> Dict[str, str]:
        return {"Authorization": f"Token {self.token}"}


@dataclass(frozen=True)
class APIHeaderAuthorization(Authorization):
    """
    Provides authorization method directly from authentication headers.
    """

    #: HTTP headers
    buffer: RHeaders

    def headers(self) -> Dict[str, str]:
        return self.buffer


@dataclass(frozen=True)
class Client:
    """
    Provides a high-level client implementation for DECAF API.
    """

    #: Base API URI.
    url: str

    #: API authorization.
    auth: Authorization

    class _NullAuth(AuthBase):
        """
        Provides the no-op authentication provider implementation.
        """

        def __call__(self, r: Any) -> Any:
            return r

    #: Defines the no-op authentication provider.
    _noop_auth: ClassVar[_NullAuth] = _NullAuth()

    #: Defines success status codes for each HTTP method.
    _successmap: ClassVar[Dict[RMethod, Set[int]]] = {
        "GET": {200},
        "POST": {200, 201, 202},
        "PUT": {200, 201, 202},
        "PATCH": {200, 201, 202},
        "DELETE": {200, 201, 202, 204},
    }

    def __post_init__(self) -> None:
        """
        Sanitizes the base API URL.

        >>> client = Client("http://example.com///", Authorization())
        >>> client.url
        'http://example.com'
        >>> client = Client("http://example.com/api//", Authorization())
        >>> client.url
        'http://example.com/api'
        """
        object.__setattr__(self, "url", re.sub(r"[/]+$", "", self.url))

    def urlize(self, path: RPath) -> str:
        """
        Builds the full URL for the given relative path or path segments.

        :param path: Relative path or path segments of the remote API endpoint.
        :return: Remote endpoint URL.

        >>> client = Client("http://example.com///", Authorization())
        >>> client.urlize("test")
        'http://example.com/test/'
        >>> client.urlize("test/")
        'http://example.com/test/'
        >>> client.urlize("/test")
        'http://example.com/test/'
        >>> client.urlize("/test/")
        'http://example.com/test/'
        >>> client.urlize("test//")
        'http://example.com/test/'
        >>> client.urlize("//test")
        'http://example.com/test/'
        >>> client.urlize("//test//")
        'http://example.com/test/'
        >>> client.urlize(["test"])
        'http://example.com/test/'
        >>> client.urlize(["test/"])
        'http://example.com/test/'
        >>> client.urlize(["/test"])
        'http://example.com/test/'
        >>> client.urlize(["/test/"])
        'http://example.com/test/'
        >>> client.urlize(["test//"])
        'http://example.com/test/'
        >>> client.urlize(["//test"])
        'http://example.com/test/'
        >>> client.urlize(["//test//"])
        'http://example.com/test/'
        >>> client.urlize(["//test//", "//test2//", "//test3/4/5//"])
        'http://example.com/test/test2/test3/4/5/'
        """
        if isinstance(path, list):
            path = "/".join(str(i).strip("/") for i in path)
        return urljoin(self.url + "/", re.sub(r"[/]*$", "/", re.sub(r"^[/]*", "", path)))

    def run(self, request: Request) -> requests.Response:
        """
        Runs the given request and returns the raw response.

        :param request: :py:class:`Request` instance to run.
        :return: Raw :py:class:`requests.Response` instance.
        :raises APIClientError: In case that there is a problem with client-server communication.
        """
        try:
            return requests.request(
                method=request.method,
                url=self.urlize(request.path),
                params=request.params,
                data=request.data,
                json=request.json,
                files=request.files,
                headers={**(request.headers or {}), **self.auth.headers()},
                timeout=request.timeout,
                auth=self._noop_auth,
            )
        except requests.exceptions.HTTPError as err:
            raise APIClientError("HTTP Error", err)
        except requests.exceptions.Timeout as err:
            raise APIClientError("Timeout Error", err)
        except requests.exceptions.ConnectionError as err:
            raise APIClientError("Connection Error", err)
        except requests.exceptions.RequestException as err:
            raise APIClientError("Request Error", err)

    def request(
        self,
        method: RMethod,
        path: RPath,
        params: Optional[RParams] = None,
        data: Any = None,
        json: Any = None,
        files: Optional[RFiles] = None,
        headers: Optional[RHeaders] = None,
        timeout: Optional[RTimeout] = None,
        asis: bool = False,
    ) -> Any:
        """
        Provides a high-level interface to run HTTP request to the remote API server.

        :param method: Request method.
        :param path: Relative path or path segments for the remote API endpoint URL.
        :param params: Request parameters, if any.
        :param data: Request data payload, if any.
        :param json: Request data payload in JSON, if any (convenience for sending ``application/json`` payloads).
        :param files: Request data payload files, if any (convenience for uploading multipart payloads).
        :param headers: Request headers.
        :param timeout: Defines the timeout, if any.
        :param asis: Whether to return response content as is or marshall it to Python object (default is ``False``).
        :return: Raw response content or Python object as per ``asis`` parameter.
        :raises APIClientError: In case that there is a problem with client-server communication.
        :raises APIServerError: In case that there is a server generated error reported via HTTP status codes.
        """
        ## Build the request, attempt to run it and get a response:
        response = self.run(
            Request(
                method=method,
                path=path,
                params=params,
                data=data,
                json=json,
                files=files,
                headers=headers,
                timeout=timeout,
            )
        )

        ## Check the status code and return if successful:
        if response.status_code in self._successmap[method]:
            if not response.content:
                return None
            return response.content if asis else response.json()

        ## We have a remote error. Encode it into an exception and raise it:
        if response.status_code >= 500:
            raise APIServerErrorBlowup("Server error", response.status_code, response.content)
        elif response.status_code == 404:
            raise APIServerErrorNotFound("Resource not found", response.status_code, response.content)
        elif response.status_code == 400:
            raise APIServerErrorBadRequest("Bad request", response.status_code, response.content, response.json())
        elif response.status_code in {401, 403, 405}:
            raise APIServerErrorBadAuthorization("Bad authorization", response.status_code, response.content)
        else:
            raise APIServerError("Unknown error", response.status_code, response.content)

    @property
    def version(self) -> str:
        """
        Returns the remote API version.
        """
        return self.request("GET", "version")["version"]  # type: ignore

    @property
    def healthcheck(self) -> str:
        """
        Performs an async healthcheck.
        """
        ## Create a healthcheck job and get its ID:
        jobid = self.request("GET", ["jobs", "healthcheck", "status"])["id"]

        ## Get job result:
        finished, result = self.get_job_result(jobid)

        ## Check:
        while not finished:
            ## Sleep a while:
            time.sleep(1)

            ## Get job result:
            finished, result = self.get_job_result(jobid)

        ## Done, return:
        return result  # type: ignore

    def get_job_result(self, jobid: str) -> Tuple[bool, Optional[Any]]:
        """
        Returns if the job is finished and associated data if so.

        :param jobid: Job identifier.
        :return: A tuple of status (``False`` meaning "pending", ``True`` meaning "finished") and optional content.
        :raises APIServerError: In case that the status is unknown.
        """
        ## Get the job status:
        content = self.request("GET", ["jobs", jobid])

        ## Get the state:
        state = content["state"]

        ## Check:
        if state == "PENDING":
            return False, None
        elif state == "SUCCESS":
            return True, content["result"]
        else:
            raise APIServerError("Unknown response from Job status endpoint", -1, content)

    @classmethod
    def from_profile(cls, name: str, path: Optional[Path] = None) -> "Client":
        """
        Attempts the create a :py:class:`Client` instance for the given profile name.

        :param name: Profile name.
        :param path: Optional path to the configuration file (default is ``~/.decaf.json``).
        :return: A :py:class:`Client` instance.
        :raises FileNotFoundError: In case that the configuration file is not found.
        :raises KeyError: In case that the profile is not found.
        """
        ## If we don't have a configuration path, use the default:
        if path is None:
            path = Path.home() / ".decaf.json"

        ## Attempt to read in the configuration:
        with path.open() as ifile:
            profile = {p["name"]: p for p in loadjson(ifile)["profiles"]}[name]

        ## Build the client and return:
        return Client(profile["url"], APIKeyAuthorization(key=profile["key"], scr=profile["secret"]))

    @classmethod
    def from_apikey(cls, url: str, key: str, secret: str) -> "Client":
        """
        Attempts the create a :py:class:`Client` instance for the given API key/secret.

        :param url: Base API url.
        :param key: API key.
        :param secret: API secret.
        :return: A :py:class:`Client` instance.
        """
        return Client(url, APIKeyAuthorization(key, secret))

    @classmethod
    def from_apitoken(cls, url: str, token: str) -> "Client":
        """
        Attempts the create a :py:class:`Client` instance for the given API token.

        Note that API tokens have shorter expiry than API keys. You may wish to choose API keys for clients with
        longer life time.

        :param url: Base API url.
        :param token: API token.
        :return: A :py:class:`Client` instance.
        """
        return Client(url, APITokenAuthorization(token))

    @classmethod
    def from_headers(cls, url: str, headers: RHeaders) -> "Client":
        """
        Attempts the create a :py:class:`Client` instance for the given HTTP headers.

        :param url: Base API url.
        :param headers: HTTP authentication headers.
        :return: A :py:class:`Client` instance.
        """
        return Client(url, APIHeaderAuthorization(headers))


#: Defines a generic type alias.
_T = TypeVar("_T")


def query(func: Callable[..., _T]) -> Callable[..., _T]:
    """
    Decorates a query method of an endpoint.

    :param func: method to be decorated.
    :return: Decorated method.
    """
    setattr(func, "__decaf_endpoint_method_query__", True)
    return func


def command(func: Callable[..., _T]) -> Callable[..., _T]:
    """
    Decorates a command method of an endpoint.

    :param func: method to be decorated.
    :return: Decorated method.
    """
    setattr(func, "__decaf_endpoint_method_command__", True)
    return func


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


class BaseUpdateForm(BaseModel):
    """
    Provides a base class for standard DECAF form models for resource updation.
    """

    pass


class BasePatchForm(BaseModel):
    """
    Provides a base class for standard DECAF form models for resource patching.
    """

    pass


#: Defines a type variable for :py:class:`BaseResource` implementations.
_R = TypeVar("_R", bound=BaseResource)

#: Defines a type variable for :py:class:`BaseCreateForm` implementations.
_C = TypeVar("_C", bound=BaseCreateForm)

#: Defines a type variable for :py:class:`BaseUpdateForm` implementations.
_U = TypeVar("_U", bound=BaseUpdateForm)

#: Defines a type variable for :py:class:`BasePatchForm` implementations.
_P = TypeVar("_P", bound=BasePatchForm)

#: Defines a type variable for resource identifiers.
_I = TypeVar("_I", bound=Union[str, int])


@dataclass(frozen=True)
class Endpoint:
    """
    Provides a base endpoint class.
    """

    __slots__ = ["client"]

    #: Underlying client.
    client: Client

    #: Base path segment for the remote resource URI.
    endpoint: ClassVar[str]


class ResourceEndpoint(Generic[_R], Endpoint):
    """
    Provides a base class for resource endpoints.
    """

    #: Resource model type.
    resource: ClassVar[Type[_R]]


class ResourceListEndpoint(ResourceEndpoint[_R]):
    """
    Provides a base class for resource endpoints with ``list`` query method.
    """

    @query
    def list(self, params: Optional[RParams] = None) -> Iterable[_R]:
        """
        Lists resources.

        :param params: Query parameters.
        :return: An iterable of resources.
        :raises APIClientError: In case that there is a problem with client-server communication.
        :raises APIServerError: In case that there is a server generated error reported via HTTP status codes.
        """
        return (
            self.resource(**i)
            for i in self.client.request("GET", self.endpoint, params={**(params or {}), "page_size": "-1"})
        )


class ResourceRetrieveEndpoint(Generic[_I, _R], ResourceEndpoint[_R]):
    """
    Provides a base class for resource endpoints with ``retrieve`` query method.
    """

    @query
    def retrieve(self, ident: _I) -> Optional[_R]:
        """
        Attempts to retrieve the resource identified by the given identifier.

        :param ident: Resource identifier.
        :return: Resource if found, ``None`` otherwise.
        :raises APIClientError: In case that there is a problem with client-server communication.
        :raises APIServerError: In case that there is a server generated error reported via HTTP status codes.
        """
        try:
            return self.resource(**self.client.request("GET", [self.endpoint, ident]))
        except APIServerErrorNotFound:
            return None


class ResourceCreateEndpoint(Generic[_C, _R], ResourceEndpoint[_R]):
    """
    Provides a base class for resource endpoints with ``create`` command method.
    """

    @command
    def create(self, form: _C) -> _R:
        """
        Attempts to create a new resource with the given form data.

        :param form: Resource create form instance.
        :return: Resource if successfully created.
        :raises APIClientError: In case that there is a problem with client-server communication.
        :raises APIServerError: In case that there is a server generated error reported via HTTP status codes.
        """
        return self.resource(**self.client.request("POST", self.endpoint, json=_form_payload(form)))


class ResourceUpdateEndpoint(Generic[_I, _U, _R], ResourceEndpoint[_R]):
    """
    Provides a base class for resource endpoints with ``update`` command method.
    """

    @command
    def update(self, ident: _I, form: _U) -> _R:
        """
        Attempts to update an existing resource with the given form data.

        :param ident: Identifier of the resource to update.
        :param form: Resource update form instance.
        :return: Resource if successfully updated.
        :raises APIClientError: In case that there is a problem with client-server communication.
        :raises APIServerError: In case that there is a server generated error reported via HTTP status codes.
        """
        return self.resource(**self.client.request("PUT", [self.endpoint, ident], json=_form_payload(form)))


class ResourcePatchEndpoint(Generic[_I, _P, _R], ResourceEndpoint[_R]):
    """
    Provides a base class for resource endpoints with ``patch`` command method.
    """

    @command
    def patch(self, ident: _I, form: _P) -> _R:
        """
        Attempts to patch an existing resource with the given form data.

        :param ident: Identifier of the resource to patch.
        :param form: Resource patch form instance.
        :return: Resource if successfully patched.
        :raises APIClientError: In case that there is a problem with client-server communication.
        :raises APIServerError: In case that there is a server generated error reported via HTTP status codes.
        """
        return self.resource(**self.client.request("PATCH", [self.endpoint, ident], json=_form_payload(form)))


class DeleteEndpoint(Generic[_I], Endpoint):
    """
    Provides a base class for resource endpoints with ``delete`` command method.
    """

    @command
    def delete(self, ident: _I) -> None:
        """
        Attempts to delete the resource identified by the given identifier.

        :param ident: Identifier of the resource to delete.
        :raises APIClientError: In case that there is a problem with client-server communication.
        :raises APIServerError: In case that there is a server generated error reported via HTTP status codes.
        """
        self.client.request("DELETE", [self.endpoint, ident])


class StandardResourceEndpoint(
    Generic[_I, _C, _U, _P, _R],
    ResourceListEndpoint[_R],
    ResourceRetrieveEndpoint[_I, _R],
    ResourceCreateEndpoint[_C, _R],
    ResourceUpdateEndpoint[_I, _U, _R],
    ResourcePatchEndpoint[_I, _P, _R],
    DeleteEndpoint[_I],
    ResourceEndpoint[_R],
):
    """
    Provides a generic base endpoint class definition for standard resources with listing, retrieval, creation,
    updation, patching and deletion queries/commands.
    """

    pass


def _form_payload(form: Union[BaseCreateForm, BaseUpdateForm, BasePatchForm]) -> Dict[str, Any]:
    """
    Compiles HTTP payload from the given form instance.

    This function omits missing values.

    :param form: Form instance.
    :return: A dictionary of form field name and corresponding value.
    """
    return {k: v for k, v in form if not isinstance(v, Missing)}


class Missing:
    """
    Provides a placeholder value for missing field values.
    """

    @classmethod
    def field(cls) -> Any:
        """
        Provides a convenience method for creating a ``pydantic`` field for fields defaulting to missing value.

        :return: :py:class:`Field` with missing value as default.
        """
        return Field(cls())

    @classmethod
    def __get_validators__(cls) -> Generator[Any, None, None]:
        """
        Makes this class a first class ``pydantic`` field value class.

        :return: Validators.
        """
        yield cls.validate

    @staticmethod
    def validate(v: Any) -> "Missing":
        """
        Checks if the given value is a :py:class:`Missing` instance and returns it as is if so.

        :param v: Value to be checked.
        :return: Value.
        :raises TypeError: In case that the given value is not a :py:class:`Missing` instance.
        """
        if isinstance(v, Missing):
            return v
        raise TypeError("'Missing' instance required")
