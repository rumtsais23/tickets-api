MOCK_MODE = True
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_text(input_text):
    if MOCK_MODE:
        return f"[MOCK] Analyzed text: {input_text}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": input_text}]
    )
    return response.choices[0].message.content


def analyze_code(input_code):
    if MOCK_MODE:
        return f"[MOCK] Code analysis: {input_code}"

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=input_code
    )
    return response.output_text