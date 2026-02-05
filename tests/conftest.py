import pytest
from pyolxbr.oauth import OlxOAuth


@pytest.fixture
def oauth() -> OlxOAuth:
    return OlxOAuth(
        client_id="test_client_id",
        client_secret="test_client_secret",
        redirect_uri="https://example.com/callback",
    )
