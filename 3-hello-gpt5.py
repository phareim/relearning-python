from openai import OpenAI
client = OpenAI()

response = client.responses.create(
    model="gpt-5-nano",
    input="Say hello to the world in a fun way!"
)

print(response.output_text)