import pytest
import respx

from httpx import Response

from pyolxbr.config import TOKEN_URL
from pyolxbr.exceptions import OlxAuthError
from pyolxbr.oauth import OlxOAuth

def test_authorization_url(oauth: OlxOAuth):
    url = oauth.get_authorization_url(
        scope="basic_user_info",
        state="abc123",
    )

    assert "response_type=code" in url
    assert "client_id=test_client_id" in url
    assert "redirect_uri=https%3A%2F%2Fexample.com%2Fcallback" in url
    assert "scope=basic_user_info" in url
    assert "state=abc123" in url

@pytest.mark.asyncio
@respx.mock
async def test_exchange_code_for_token_success(oauth: OlxOAuth):
    respx.post(TOKEN_URL).mock(
        return_value=Response(
            200,
            json={
                "access_token": "access_token_123",
                "token_type": "Bearer",
                "expires_in": 3600,
            },
        )
    )

    token = await oauth.exchange_code_for_token("auth_code_123")

    assert token["access_token"] == "access_token_123"
    assert token["token_type"] == "Bearer"

@pytest.mark.asyncio
@respx.mock
async def test_exchange_code_for_token_error(oauth: OlxOAuth):
    respx.post(TOKEN_URL).mock(
        return_value=Response(400, text="invalid_grant")
    )

    with pytest.raises(OlxAuthError):
        await oauth.exchange_code_for_token("invalid_code")