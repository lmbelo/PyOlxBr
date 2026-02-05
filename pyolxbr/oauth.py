import httpx
from typing import Optional
from urllib.parse import urlencode

from .config import AUTH_BASE_URL, TOKEN_URL
from .exceptions import OlxAuthError

class OlxOAuth:

    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    def get_authorization_url(self, scope: str, state: Optional[str] = None) -> str:
        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": scope,
        }

        if state:
            params["state"] = state

        return f"{AUTH_BASE_URL}?{urlencode(params)}"
    
    async def exchange_code_for_token(self, code: str) -> dict:
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
        }

        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.post(TOKEN_URL, data=data)

        if response.status_code != 200:
            raise OlxAuthError(response.text)
        
        return response.json()