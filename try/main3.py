import openai
import json
import os
import dotenv

dotenv.load()


# Set up the OpenAI API credentials
openai.api_key = os.getenv("OPENAI_API_KEY")
print(openai.api_key)

with open("./TG_MinerRepair.json", "r") as f:
    json_data = json.load(f)

# Define your prompt and parameters
prompt = "What are several main topics of this group chat?"
params = {
    "engine": "davinci",
    "temperature": 0.7,
    "max_tokens": 1024,
    "n": 1,
    "stop": None,
    "prompt": prompt,
}

# Add the JSON data to the parameters
params["files"] = json_data

# Generate a response to the prompt using the OpenAI API
response = openai.Completion.create(**params)

# Extract the answer from the response
answer = response.choices[0].text.strip()

# Print the answer
print(answer)
