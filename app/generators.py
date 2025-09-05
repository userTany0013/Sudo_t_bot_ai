from openai import AsyncOpenAI
from config import AITOKEN, PROXY

import httpx

client = AsyncOpenAI(api_key=AITOKEN,
                     http_client=httpx.AsyncClient(proxies=PROXY,
                                                   transport=httpx.HTTPTransport(local_address='0.0.0.0.')))


async def gpt_text(reg, model):
    completion = await client.chat.completions.create(
        messages=[{'role': 'user', 'content': reg}],
        model=model
    )
    return {'response': completion.choices[0].message.content,
            'usage': completion.usage.total_tokens}