import json
import os
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


def get_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is missing. Create a .env file or set the environment variable."
        )
    return OpenAI(api_key=api_key)


def call_json_model(system_prompt: str, user_prompt: str, model: str = "gpt-4o-mini") -> dict[str, Any]:
    client = get_client()

    response = client.chat.completions.create(
        model=model,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
    )

    content = response.choices[0].message.content
    if content is None:
        raise RuntimeError("Model returned empty response.")

    return json.loads(content)


def call_text_model(system_prompt: str, user_prompt: str, model: str = "gpt-4o-mini") -> str:
    client = get_client()

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
    )

    content = response.choices[0].message.content
    if content is None:
        raise RuntimeError("Model returned empty response.")

    return content
