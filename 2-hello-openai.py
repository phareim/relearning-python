from openai import OpenAI

# Initialize client (reads API key from env variable: OPENAI_API_KEY)
client = OpenAI()

# Ask the model for a message
response = client.chat.completions.create(
    model="gpt-4o-mini",  # small, fast model
    messages=[
        {"role": "system", "content": "You are a friendly assistant."},
        {"role": "user", "content": "Say hello to the world in a fun way!"}
    ]
)

# Grab the text of the first choice
message = response.choices[0].message.content

print(message)