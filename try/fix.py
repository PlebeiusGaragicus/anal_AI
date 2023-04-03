import openai

# Set up your OpenAI API key
openai.api_key = "YOUR_API_KEY"

# Define your training data as a list of JSON objects
training_data = [
    {"text": "The quick brown fox jumps over the lazy dog", "label": "animal"},
    {"text": "An apple a day keeps the doctor away", "label": "food"},
    {"text": "The cat in the hat", "label": "animal"},
    {"text": "To be or not to be, that is the question", "label": "philosophy"}
]

# Create a new training run with your custom dataset
training_run = openai.api.Training.create(
    model="text-davinci-002",
    dataset="my-dataset",
    data=training_data,
    description="My custom dataset"
)

# Get the ID of the training run
training_run_id = training_run["id"]

# Wait for the training run to complete
while True:
    training_run = openai.api.Training.retrieve(training_run_id)
    if training_run["status"] == "succeeded":
        break
    if training_run["status"] == "failed":
        raise ValueError("Training failed")

# Use the trained model to generate text completions
prompt = "Label: food\nQuestion: What's the best food?\nAnswer:"
response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=prompt,
    temperature=0.5,
    max_tokens=50,
    n=1,
    stop=None,
    model=training_run.model.id
)

# Extract the generated text from the response
generated_text = response.choices[0].text

print(generated_text)
