"""
This module provides the essential machinery to perform remote API requests.
"""

__all__ = [
    "APIClientError",
    "APIServerError",
    "APIServerErrorBadAuthorization",
    "APIServerErrorBadRequest",
    "APIServerErrorBlowup",
    "APIServerErrorNotFound",
    "Client",
    "Error",
    "RFiles",
    "RHeaders",
    "RMethod",
    "RParams",
    "RPath",
    "RTimeout",
    "Request",
]

import re
import time
from dataclasses import dataclass
from json import load as loadjson
from pathlib import Path
from typing import Any, BinaryIO, ClassVar, Dict, List, Optional, Set, TextIO, Tuple, Union
from urllib.parse import urljoin

import requests
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
RPath = Union[str, List[str]]

#: Defines a type alias for query-string parameters.
RParams = Dict[str, str]

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


@dataclass(frozen=True)
class Client:
    """
    Provides a high-level client implementation for DECAF API.
    """

    #: Defines the base API URI.
    url: str

    #: Defines the API key.
    key: str

    #: Defines the API secret.
    scr: str

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

        >>> client = Client("http://example.com///", "key", "scr")
        >>> client.url
        'http://example.com'
        >>> client = Client("http://example.com/api//", "key", "scr")
        >>> client.url
        'http://example.com/api'
        """
        object.__setattr__(self, "url", re.sub(r"[/]+$", "", self.url))

    def urlize(self, path: RPath) -> str:
        """
        Builds the full URL for the given relative path or path segments.

        :param path: Relative path or path segments of the remote API endpoint.
        :return: Remote endpoint URL.

        >>> client = Client("http://example.com///", "key", "scr")
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
            path = "/".join(i.strip("/") for i in path)
        return urljoin(self.url + "/", re.sub(r"[/]*$", "/", re.sub(r"^[/]*", "", path)))

    @property
    def _auth_head_value(self) -> str:
        """
        ``Authentication`` header value.
        """
        return f"Key {self.key}:{self.scr}"

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
                headers={**(request.headers or {}), "Authorization": self._auth_head_value},
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
        return Client(url=profile["url"], key=profile["key"], scr=profile["secret"])
