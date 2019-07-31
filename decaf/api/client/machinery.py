import json
import re
import time
import urllib.parse
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import requests
from requests import Response
from requests.auth import AuthBase


class RemoteException(Exception):
    """
    Defines a exception class for remote *DECAF* communication errors.
    """
    pass


class _NullAuth(AuthBase):
    """
    Provides the no-op authentication provider implementation.
    """

    def __call__(self, r: Any) -> Any:
        return r


#: Defines the no-op authentication provider.
_noop_auth = _NullAuth()

#: Defines a type alias for request parameters.
RParams = Optional[Dict[str, str]]

#: Defines a type alias for request data:
RData = Optional[Any]

#: Defines a type alias for request payload in JSON.
RJson = Optional[Any]

#: Defines a type alias for request files.
RFiles = Optional[Dict[str, Any]]

#: Defines a type alias for request headers.
RHeads = Optional[Dict[str, str]]

#: Defines a type alias for timeouts.
RTimeout = Optional[Tuple[float, float]]


@dataclass(frozen=True)
class CError(Exception):
    """
    Defines a client error.

    This is quite a generic error type which covers all communication errors.
    """

    #: Defines the description of the error.
    desc: str

    #: Defines the HTTP status code.
    status: int

    #: Defines the HTTP response payload, if any.
    rsdata: Optional[Any]


@dataclass(frozen=True)
class CRequest:
    """
    Defines a high(ish)-level client request model.
    """

    #: Defines the relative path for the remote API endpoint URL.
    endpoint: str

    #: Defines the request method.
    method: str = "GET"

    #: Defines the request parameters.
    params: RParams = None

    #: Defines the request data payload.
    data: RData = None

    #: Defines the request data payload in JSON.
    json: RJson = None

    #: Defines the request data payload files.
    files: RFiles = None

    #: Defines the request headers.
    headers: RHeads = None

    #: Defines the timeout, if any:
    timeout: RTimeout = None

    @classmethod
    def get(cls, endpoint: str, params: RParams = None, headers: RHeads = None, timeout: RTimeout = None) -> "CRequest":
        """
        Returns a client request instance for simple get requests.

        :param endpoint:    Relative path for the remote API endpoint URL.
        :param params:      Request parameters, if any.
        :param headers:     Request headers, if any.
        :param timeout:     Request timeout, if any.
        :return:            A :class:`CRequest` instance.
        """
        return cls(endpoint=endpoint, params=params, headers=headers, timeout=timeout)


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

    def build_url(self, endpoint: str) -> str:
        """
        Builds the full URL for the given endpoint.

        :param endpoint:    Remote endpoint URI path segment.
        :return:            Remote endpoint URL.
        :raises:            :class:`CError`

        >>> client = Client("http://example.com///", "key", "scr")
        >>> client.build_url("test")
        'http://example.com/test/'
        >>> client.build_url("test/")
        'http://example.com/test/'
        >>> client.build_url("/test")
        'http://example.com/test/'
        >>> client.build_url("/test/")
        'http://example.com/test/'
        >>> client.build_url("test//")
        'http://example.com/test/'
        >>> client.build_url("//test")
        'http://example.com/test/'
        >>> client.build_url("//test//")
        'http://example.com/test/'
        """
        return urllib.parse.urljoin(self.url + "/", re.sub(r"[/]*$", "/", re.sub(r"^[/]*", "", endpoint)))

    @property
    def _auth_head_value(self) -> str:
        """
        Defines the Authentication header value.
        """
        return f"Key {self.key}:{self.scr}"

    def request(self, request: CRequest) -> Response:  # noqa: ignore=C901
        """
        Provides a low level abstraction for API requests.
        """
        ## Prepare headers:
        headers = {**(request.headers or {}), "Authorization": self._auth_head_value}

        ## Prepare the request arguments:
        reqargs: Dict[str, Any] = {
            "method": request.method,
            "url": self.build_url(request.endpoint),
            "params": request.params,
            "data": request.data,
            "json": request.json,
            "files": request.files,
            "headers": headers,
            "auth": _noop_auth,
            "timeout": request.timeout,
        }

        ## Attempt to request and return:
        try:
            return requests.request(**reqargs)
        except requests.exceptions.HTTPError as err:
            raise CError(f"HTTP Error", -1, str(err))
        except requests.exceptions.Timeout as err:
            raise CError(f"Timeout Error", -1, str(err))
        except requests.exceptions.ConnectionError as err:
            raise CError(f"Connection Error", -1, str(err))
        except requests.exceptions.RequestException as err:
            raise CError(f"Request Error", -1, str(err))

    def get(self, endpoint: str, params: RData = None, headers: RHeads = None, timeout: RTimeout = None) -> Any:
        """
        Issues a GET request to the remote API endpoint which returns a JSON response.

        This is a convenience method. For more control over the request, use :meth:`Client.request` method.

        :param endpoint:    Relative path for the remote API endpoint URL.
        :param params:      Request parameters, if any.
        :param headers:     Request headers, if any.
        :param timeout:     Request timeout, if any.
        :return:            Response data as a Python primitive.
        :raises:            :class:`CError`
        """
        ## Attempt to get the response:
        response = self.request(CRequest.get(endpoint, params, headers, timeout))

        ## Check the status code:
        if response.status_code != 200:
            raise CError("Error while consuming remote endpoint", response.status_code, response.content)

        ## Return the data:
        return response.json()

    def post(self, endpoint: str, params: RData = None, headers: RHeads = None, json: RJson = None, timeout: RTimeout = None) -> Any:  # noqa: E501
        """
        Issues a POST request to the remote API endpoint which returns a JSON response.

        This is a convenience method. For more control over the request, use :meth:`Client.request` method.

        :param endpoint:    Relative path for the remote API endpoint URL.
        :param params:      Request parameters, if any.
        :param headers:     Request headers, if any.
        :param json:        Data which can be marshalled into a JSON payload.
        :param timeout:     Request timeout, if any.
        :return:            Response data as a Python primitive.
        :raises:            :class:`CError`
        """
        ## Prepare the request:
        request = CRequest(endpoint, method="POST", params=params, json=json, headers=headers, timeout=timeout)

        ## Attempt to post the response:
        response = self.request(request)

        ## Check the status code:
        if response.status_code > 299:
            raise CError("Error while posting to remote endpoint", response.status_code, response.content)

        ## Return the data:
        return response.json()

    def put(self, endpoint: str, params: RData = None, headers: RHeads = None, json: RJson = None, timeout: RTimeout = None) -> Any:  # noqa: E501
        """
        Issues a PUT request to the remote API endpoint which returns a JSON response.

        This is a convenience method. For more control over the request, use :meth:`Client.request` method.

        :param endpoint:    Relative path for the remote API endpoint URL.
        :param params:      Request parameters, if any.
        :param headers:     Request headers, if any.
        :param json:        Data which can be marshalled into a JSON payload.
        :param timeout:     Request timeout, if any.
        :return:            Response data as a Python primitive.
        :raises:            :class:`CError`
        """
        ## Prepare the request:
        request = CRequest(endpoint, method="PUT", params=params, json=json, headers=headers, timeout=timeout)

        ## Attempt to post the response:
        response = self.request(request)

        ## Check the status code:
        if response.status_code > 299:
            raise CError("Error while posting to remote endpoint", response.status_code, response.content)

        ## Return the data:
        return response.json()

    @property
    def version(self) -> str:
        """
        Returns the remote API version.
        """
        return self.get("version")["version"]  # type: ignore

    @property
    def healthcheck(self) -> str:
        """
        Performs an async healthcheck.
        """
        ## Create a healthcheck job and get its ID:
        jobid = self.get("jobs/healthcheck/status")["id"]

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
        """
        ## Get the job status:
        content = self.get(f"/jobs/{jobid}/")

        ## Get the state:
        state = content["state"]

        ## Check:
        if state == "PENDING":
            return False, None
        elif state == "SUCCESS":
            return True, content["result"]
        else:
            raise CError("Unknown response from Job status endpoint", -1, content)

    @classmethod
    def from_profile(cls, name: str, cpath: Optional[Path] = None) -> "Client":
        """
        Attempts the create a `Client` for the given profile name.
        """
        ## If we don't have a configuration path, use the default:
        if cpath is None:
            cpath = Path.home() / ".decaf.json"

        ## Attempt to read in the configuration:
        with cpath.open() as ifile:
            profile = {p["name"]: p for p in json.load(ifile)["profiles"]}[name]

        ## Build the client and return:
        return Client(url=profile["url"], key=profile["key"], scr=profile["secret"])
