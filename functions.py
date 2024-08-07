import json
import requests
import os
from openai import OpenAI
from prompts import  assistant_instructions
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']


# Init OpenAI Client
client = OpenAI(api_key=OPENAI_API_KEY)




def create_assistant(client):
    assistant_file_path = 'assistant.json'
    
    # Check if the assistant.json file exists
    if os.path.exists(assistant_file_path):
        with open(assistant_file_path, 'r') as file:
            assistant_data = json.load(file)
            assistant_id = assistant_data['assistant_id']
            print("Loaded existing assistant ID.")
    else:
        # Create a new assistant with a specific knowledge document
        # file = client.files.create(file=open("california_real_estate.docx", "rb"), purpose='assistants')
        # print("File of knowledge uploaded:", file)
        
        assistant = client.beta.assistants.create(
            instructions=assistant_instructions,
            model="gpt-3.5-turbo",  # Use GPT-4 model
            tools=[
                {
                    "type": "retrieval"  # Adds the knowledge base as a tool
                },
                {
                    "type": "function",
                    "function": {
                        "name": "get_property_value_estimate",
                        "description": "Estimate the value of a property based on its location and features.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "address": {
                                    "type": "string",
                                    "description": "Address of the property."
                                },
                                "features": {
                                    "type": "object",
                                    "description": "Features of the property such as number of bedrooms, bathrooms, etc.",
                                    "properties": {
                                        "bedrooms": {
                                            "type": "integer",
                                            "description": "Number of bedrooms."
                                        },
                                        "bathrooms": {
                                            "type": "integer",
                                            "description": "Number of bathrooms."
                                        },
                                        "square_feet": {
                                            "type": "integer",
                                            "description": "Total square footage of the property."
                                        }
                                    },
                                    "required": ["bedrooms", "bathrooms", "square_feet"]
                                }
                            },
                            "required": ["address", "features"]
                        }
                    }
                }
            ],
            file_ids=[file.id]
        )
        
        # Save the new assistant ID for future use
        with open(assistant_file_path, 'w') as file:
            json.dump({'assistant_id': assistant.id}, file)
            print("Created a new assistant and saved the ID.")
        
        assistant_id = assistant.id

    return assistant_id
