from openai import AsyncOpenAI
from config import AITOKEN, PROXY

import httpx
import base64
import aiohttp
import aiofiles

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


async def gpt_image(req, model):
    response = client.images.generate(
        model=model,
        prompt=req,
        size='1024x1024',
        quality='standard',
        n=1
    )
    return {'response': response.data[0].url,
            'usage': 1}


async def encode_image(image_path):
    async with aiofiles.open(image_path, "rb") as image_file:
        return base64.b64encode(await image_file.read()).decode("utf-8")


async def gpt_vision(req, model, file):
    base64_image = await encode_image(file)

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer{AITOKEN}'
    }

    payload = {
        'model': model,
        'messages':[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_image",
                        "image_url": {'url': f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ], 'max_tokens': 300}

    if req is not None:
        payload['messages'][0]['content'].append(                    {
                        "type": "text",
                        "text": req
                    })

    async with aiohttp.ClientSession() as session:
        async with session.post('https://api.openai.com/v1/chat/completions',
                                headers=headers, json=payload) as response:
            completion = await response.json()
    return {'response': completion['choices'][0]['message']['content'],
            'usage': completion['usage']['total_tokens']}
