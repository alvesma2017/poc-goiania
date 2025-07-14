import openai
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def enviar_prompt_livre(prompt_text):
    openai.api_key = OPENAI_API_KEY

    response = openai.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "Você é um assistente jurídico especializado em licitações e contratos públicos (Lei 14.133/2021). Seja direto, objetivo e forneça o texto solicitado com clareza."},
            {"role": "user", "content": prompt_text},
        ],
        temperature=0.2,
        max_tokens=10000
    )
    return response.choices[0].message.content
