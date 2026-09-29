from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-5.6-luna",
    input="Test OK com conexao com OpenAPI"
)

print(response.output_text)