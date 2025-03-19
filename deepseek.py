# This code uses the deepseek API to generate a response to a user's input.
from openai import OpenAI

client = OpenAI(api_key="sk-9d7984a809594bf091dc6b27a28c69ab", base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a dog"},
        {"role": "user", "content": "Hello"},
    ],
    stream=False
)

print(response.choices[0].message.content)