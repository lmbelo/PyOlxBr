# PyOlxBr
Cliente Python para integração com a API do Marketplace OLX Brasil (OAuth 2.0).


## Exemplo de uso

```python
import asyncio
from pyolxbr import OlxClient

async def main():
    client = OlxClient(
        client_id="CLIENT_ID",
        client_secret="CLIENT_SECRET",
        redirect_uri="https://marketplace.auth.hook.lcapecaforte.com.br"
    )

    print(await client.authorization_url(scope="basic_user_info"))

    token = await client.authenticate(code="AUTH_CODE")
    print(token)

    await client.close()

asyncio.run(main())
```
