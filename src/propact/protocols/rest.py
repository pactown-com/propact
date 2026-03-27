"""REST protocol implementation for Propact."""

# Constants
HTTP_STATUS_OK = 200

from typing import Dict, Any, Optional, Union
from dataclasses import dataclass
from enum import Enum


class HTTPMethod(Enum):
    """HTTP methods supported by REST protocol."""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"


@dataclass
class RESTRequest:
    """REST request structure."""
    method: HTTPMethod
    url: str
    headers: Optional[Dict[str, str]] = None
    params: Optional[Dict[str, Any]] = None
    body: Optional[Union[str, Dict[str, Any]]] = None


@dataclass
class RESTResponse:
    """REST response structure."""
    status_code: int
    headers: Dict[str, str]
    body: Optional[Union[str, Dict[str, Any]]] = None
    success: bool = False


class RESTProtocol:
    """Handles REST API communication within Protocol Pact."""
    
    def __init__(self, base_url: Optional[str] = None, 
                 default_headers: Optional[Dict[str, str]] = None):
        """Initialize RESTProtocol.
        
        Args:
            base_url: Base URL for all requests.
            default_headers: Default headers for all requests.
        """
        self.base_url = base_url
        self.default_headers = default_headers or {}
        
    async def execute(self, request: RESTRequest) -> RESTResponse:
        """
        Execute a REST request.
        
        Args:
            request: REST request to execute.
            
        Returns:
            REST response.
        """
        # Placeholder for actual HTTP request execution
        # In a real implementation, you would use httpx or aiohttp
        
        url = request.url
        if self.base_url and not request.url.startswith(('http://', 'https://')):
            url = f"{self.base_url.rstrip('/')}/{request.url.lstrip('/')}"
            
        # Merge headers
        headers = {**self.default_headers}
        if request.headers:
            headers.update(request.headers)
            
        # Simulate response
        return RESTResponse(
            status_code=HTTP_STATUS_OK,
            headers={"content-type": "application/json"},
            body={"message": "REST protocol not yet implemented", 
                  "url": url,
                  "method": request.method.value},
            success=True
        )
        
    async def get(self, url: str, params: Optional[Dict[str, Any]] = None,
                 headers: Optional[Dict[str, str]] = None) -> RESTResponse:
        """Execute GET request."""
        request = RESTRequest(
            method=HTTPMethod.GET,
            url=url,
            params=params,
            headers=headers
        )
        return await self.execute(request)
        
    async def post(self, url: str, body: Optional[Union[str, Dict[str, Any]]] = None,
                  headers: Optional[Dict[str, str]] = None) -> RESTResponse:
        """Execute POST request."""
        request = RESTRequest(
            method=HTTPMethod.POST,
            url=url,
            body=body,
            headers=headers
        )
        return await self.execute(request)
        
    async def put(self, url: str, body: Optional[Union[str, Dict[str, Any]]] = None,
                 headers: Optional[Dict[str, str]] = None) -> RESTResponse:
        """Execute PUT request."""
        request = RESTRequest(
            method=HTTPMethod.PUT,
            url=url,
            body=body,
            headers=headers
        )
        return await self.execute(request)
        
    async def delete(self, url: str, headers: Optional[Dict[str, str]] = None) -> RESTResponse:
        """Execute DELETE request."""
        request = RESTRequest(
            method=HTTPMethod.DELETE,
            url=url,
            headers=headers
        )
        return await self.execute(request)
