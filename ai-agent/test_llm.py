from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-5.6-luna",
    input="Responda apenas: conexão com LLM funcionando"
)

print(response.output_text)