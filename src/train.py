import openai
import json
import os
import sys
import dotenv

##############################################
if __name__ == "__main__":

    dotenv.load()

    # Set up the OpenAI API credentials
    key = os.getenv("OPENAI_API_KEY")
    if key is None:
        print("The OPENAI_API_KEY environment variable is not set.")
        sys.exit(1)

    openai.api_key = key

    # Check if a file name was passed as an argument
    if len(sys.argv) == 1:
        print("Please pass the name of the JSON file as an argument.")
        sys.exit(1)

    # the first parameter is the name of the file
    file_name = sys.argv[1]

    if file_name.split(".")[-1] != "json":
        print("The file must be a JSON file.")
        sys.exit(1)


    # Load the JSON data from a file
    with open(file_name, "r") as f:
        data = json.load(f)

    # Create a new training run
    training_run = openai.Model.create(
        model="text-davinci-003",
        dataset="TG_MinerRepair",
        data=data,
        description="A Telegram chat group history about Bitcoin Miner Repair"
    )

    # Get the ID of the training run
    training_run_id = training_run["id"]

    print(f"Training run ID: {training_run_id}")
