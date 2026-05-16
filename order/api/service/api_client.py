import httpx
from typing import Any, Dict, Optional
from fastapi import Request

async def api_client(
        request: Request, 
        method: str,
        url: str,
        data: Optional[Dict[str, Any]] = None, 
        params: Optional[Dict[str, Any]] = None, 
        headers: Optional[Dict[str, Any]] = None, 
        timeout: int = 30):
    
    #TODO:route through sidecar
    
    try:

        requests_client: httpx.AsyncClient = request.app.requests_client

        response = await requests_client.request(
            method=method.upper(),
            url=url,
            data=data,
            params=params,
            headers=headers,
            timeout=timeout)

        #TODO:contain response in a model
        response.raise_for_status()
        return response.json()
        
    except Exception as e:
        raise
    
    