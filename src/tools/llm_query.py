from openai import AsyncOpenAI
from dotenv import load_dotenv

import os
import asyncio

load_dotenv()

model_settings = {
    "model":os.environ.get("MODEL_NAME"),
    "temperature": 0.2,
    "timeout": 60,
    "max_tokens": 1024
}

async def llm_retrieve(prompt: str) -> str:
    client = AsyncOpenAI(api_key=os.environ.get("API_KEY"), base_url=os.environ.get("BASE_URL"))

    response = await client.chat.completions.create(
        messages=[
            {
                "role": "user", 
                "content": prompt
            }
        ],
        **model_settings
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    asyncio.run(llm_retrieve("Hello world"))
