import openai
import json
import os
import dotenv

dotenv.load()


# Set up the OpenAI API credentials
openai.api_key = os.getenv("OPENAI_API_KEY")
print(openai.api_key)

# Load the JSON data from a file
with open("./TG_MinerRepair.json", "r") as f:
    data = json.load(f)

# Ask OpenAI a question about the data
response = openai.Completion.create(
    engine="davinci",
    prompt="What are the main topics in the chat thread?",
    data=[["data", json.dumps(data)]],
    max_tokens=50,
    n=1,
    stop=None,
    temperature=0.7,
)

# Print the response
print(response.choices[0].text)
