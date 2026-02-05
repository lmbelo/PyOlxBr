from typing import Optional
from .oauth import OlxOAuth

class OlxClient:

    def __init__(
        self, 
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        access_token: Optional[str] = None,
    ):
        self.oauth = OlxOAuth(client_id, client_secret, redirect_uri)
        self.access_token = access_token

    def authorization_url(self, scope: str, state: Optional[str] = None) -> str:
        return self.oauth.get_authorization_url(scope, state)
    
    async def authenticate(self, code: str) -> dict:
        token_data = await self.oauth.exchange_code_for_token(code)
        self.access_token = token_data.get("access_token")

        return token_data