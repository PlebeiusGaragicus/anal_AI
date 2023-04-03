# this module inputs a JSON file that is an export of a telegram chat and cleans up the data so that it can be used to train a model to generate a summary of the chat.
#
# {
#  "name": "Immersion Cooling Technology Talk",
#  "type": "public_supergroup",
#  "id": 1482056085,
#  "messages": [
#   {
#    "id": 1,
#    "type": "service",
#    "date": "2019-04-04T10:45:05",
#    "date_unixtime": "1554399905",
#    "actor": "Immersion Cooling Technology Talk",
#    "actor_id": "channel1482056085",
#    "action": "migrate_from_group",
#    "title": "Immersion Cooling Technology Talk",
#    "text": "",
#    "text_entities": []
#   },
#   {
#    "id": 3,
#    "type": "message",
#    "date": "2019-04-04T10:52:24",
#    "date_unixtime": "1554400344",
#    "from": "Scott Offord",
#    "from_id": "user509128351",
#    "photo": "(File not included. Change data exporting settings to download.)",
#    "width": 400,
#    "height": 400,
#    "text": "Welcome to “Immersion Cooling Technology Talk”. Please share your project here and discuss freely about liquid cooling for crypto and other applications.",
#    "text_entities": [
#     {
#      "type": "plain",
#      "text": "Welcome to “Immersion Cooling Technology Talk”. Please share your project here and discuss freely about liquid cooling for crypto and other applications."
#     }
#    ]
#   },
#   {
#    "id": 5,
#    "type": "service",
#    "date": "2019-04-04T11:00:08",
#    "date_unixtime": "1554400808",
#    "actor": "CoastBTC",
#    "actor_id": "user386894381",
#    "action": "invite_members",
#    "members": [
#     "CoastBTC"
#    ],
#    "text": "",
#    "text_entities": []
#   },
#   {
#    "id": 6,
#    "type": "service",
#    "date": "2019-04-04T11:02:31",
#    "date_unixtime": "1554400951",
#    "actor": "Rasmus",
#    "actor_id": "user773781447",
#    "action": "invite_members",
#    "members": [
#     "Rasmus"
#    ],
#    "text": "",
#    "text_entities": []
#   },
#  ]
# }
#

import sys
import json
import re

import networkx as nx
from networkx.readwrite import json_graph

class TelegramJSONCleaner:

#################################
    def keep_messages(json_data):
        # This function takes a JSON file and returns a list of messages

        template = {
            "id": 0,
            "from": "",
            "from_id": "",
            "text": "",
        }

        message_list = []

        # Create a directed graph for the conversation
        G = nx.DiGraph()

        for message in json_data["messages"]:
            if message["type"] != "message":
                continue

            if message["text_entities"] == []:
                continue

            # ensure it's a text message, not a mention or something else
            if type(message["text"]) == list:
                # print(f"skipping message {message['id']}")
                # exit(1)
                continue


            # Add nodes to the graph for each message
            node_data = template.copy()
            node_data["id"] = message["id"]
            node_data["from"] = message["from"]
            node_data["from_id"] = message["from_id"]

            # remove emoji from text
            no_emoji = re.sub(r'[^\x00-\x7F]+',' ', message["text"])
            node_data["text"] = no_emoji
            # node_data["text"] = message["text"]

            if 'reply_to_message_id' in message:
                node_data["reply_to_message_id"] = message["reply_to_message_id"]
        
            G.add_node(message['id'], **node_data)
            message_list.append(node_data)
        # end for

        # Add edges between messages based on 'reply_to_message_id' field
        for message in message_list:

            if 'reply_to_message_id' in message:
                print(f"adding edge from {message['reply_to_message_id']} to {message['id']}")
                G.add_edge(message['reply_to_message_id'], message['id'])



            # message_list.append(tidied)
        # end for


        # Convert the graph to a JSON data file
        graph_data = json_graph.node_link_data(G)
        return graph_data

        # return message_list

##############################
    def clean_json(json_data):
        # This function takes a JSON file and returns a list of messages

        messages = json_data["messages"]

        message_list = []

        for message in messages:
            message_type = message["type"]

            # Check if the message is a service message
            if message_type == "service":
                # Get the action
                action = message["action"]

                # Check if the action is a member joining
                if action == "invite_members":
                    # Get the member name
                    member_name = message["members"][0]

                    # Create a message
                    message = f"{member_name} joined the chat."

                    # Add the message to the list
                    message_list.append(message)

                # Check if the action is a member leaving
                elif action == "leave_members":
                    # Get the member name
                    member_name = message["members"][0]

                    # Create a message
                    message = f"{member_name} left the chat."

                    # Add the message to the list
                    message_list.append(message)

            # Check if the message is a message
            elif message_type == "message":
                # Get the message text
                message_text = message["text"]

                # Add the message to the list
                message_list.append(message_text)

        return message_list

###################################################
def main():
    # if no arguments are passed, print the help message
    if len(sys.argv) == 1:
        print("\n\nThis script takes a Telegram JSON file and returns a clean JSON file.")
        print("Usage: python3 clean_telegram_json.py <file_name>")
        print("Example: python3 clean_telegram_json.py telegram_chat.json")
        print("This will create a file called telegram_chat_clean.json")
        return

    # the first parameter is the name of the file
    file_name = sys.argv[1].split(".json")[0]
    print(f"file_name: {file_name}")
    print(f"opening file: {file_name}.json")

    # Load the JSON data from a file
    with open(f"./{file_name}.json", "r") as f:
        data = json.load(f)

    ##### CLEAN THE DATA #####
    clean_data = TelegramJSONCleaner.keep_messages(data)

    # Save the clean data to a file
    with open(f"./{file_name}_clean.json", "w") as f:
        json.dump(clean_data, f)



###################################################
if __name__ == "__main__":
    main()
