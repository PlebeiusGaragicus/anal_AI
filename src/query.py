import openai

# Ask the model a question
question = "What's the best food?"
response = openai.api.Completion.create(
    model="text-davinci-002",
    prompt=f"Label: food\nQuestion: {question}\nAnswer:",
    temperature=0.5,
    max_tokens=50,
    n=1,
    stop=None
)

# Get the answer from the response
answer = response["choices"][0]["text"].strip()
print(answer)
