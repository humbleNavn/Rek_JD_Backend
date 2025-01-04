import json
from openai import OpenAI
from typing import List, Dict
from dotenv import load_dotenv



client = OpenAI()
oai_model = 'gpt-4o'

load_dotenv('.env', override=True)

def call_llm(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model=oai_model,
            messages=[{"role": "system", "content": prompt}],
            temperature=1,
            top_p=0.1
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return str(e)

