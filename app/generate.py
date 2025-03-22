from openai import AsyncOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

ai_token = os.getenv("AI_TOKEN")

client = AsyncOpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=ai_token,
)

async def ai_generate(text: str):
  prompt = """
      Ты — вежливый и дружелюбный собеседник. Отвечай спокойно и уважительно.
      Теперь отвечай в этом стиле.
      """

  completion = await client.chat.completions.create(
    model="deepseek/deepseek-chat",
    messages=[
      {"role": "system", "content": prompt},
      {"role": "user", "content": text}
    ]
  )

  print(completion)
  return completion.choices[0].message.content