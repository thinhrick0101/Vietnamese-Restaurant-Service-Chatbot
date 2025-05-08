from dotenv import load_dotenv
import os
import json
from copy import deepcopy
from agent.utils import get_chatbot_response
from openai import OpenAI

# Load environment variables from the .env file
load_dotenv()

class SecureAgent:
    """
    SecureAgent is an AI assistant that determines whether user queries
    are related to our restaurant. It allows questions about location,
    working hours, menu items, orders, and recommendations, while disallowing
    queries on unrelated topics or inquiries about staff or recipe details.
    """

    def __init__(self):
        # Initialize the OpenAI client with API key and base URL from environment variables.
        self.client = OpenAI(
            api_key=os.getenv("RUNPOD_TOKEN"),
            base_url=os.getenv("RUNPOD_CHATBOT_URL"),
        )
        self.model_name = os.getenv("MODEL_NAME")
    
    def get_response(self, messages):
        """
        Processes the last few conversation messages by prepending a system prompt.
        Retrieves the AI's output and formats it into the expected dictionary structure.
        
        Parameters:
            messages (list): List of message dictionaries from the conversation.
        
        Returns:
            dict: A dictionary containing the assistant's role, content, and memory information.
        """
        # Create a deep copy of the messages list to prevent modifications to the original data
        messages_copy = deepcopy(messages)

        # Define the system prompt to instruct the AI on acceptable queries and response format
        system_prompt = (
            "You are a helpful AI assistant for a restaurant application which serves drinks and pastries.\n"
            "Your task is to determine whether the user is asking something relevant to the restaurant or not.\n"
            "Allowed queries include:\n"
            "1. Questions about the restaurant (e.g., location, working hours, menu items, etc.).\n"
            "2. Inquiries about menu items (e.g., ingredients, details about an item).\n"
            "3. Placing an order.\n"
            "4. Asking for recommendations on what to buy.\n\n"
            "Disallowed queries include:\n"
            "1. Questions about topics unrelated to our restaurant.\n"
            "2. Questions about the staff or how to make a menu item.\n\n"
            "Your output must be in the following JSON format, with each key and value as a string. "
            "Follow the format exactly:\n"
            "{\n"
            '  "chain of thought": <your thought process>,\n'
            '  "decision": "allowed" or "not allowed",\n'
            '  "message": "Sorry, I can\'t help with that. Can I help you with your order?" (if not allowed) or leave this blank/empty for allowed queries\n'
            "}\n"
        )

        # Only consider the last three messages and prepend the system prompt
        input_messages = [{"role": "system", "content": system_prompt}] + messages_copy[-3:]

        # Get the response from the chatbot using the provided client, model, and input messages
        chatbot_response = get_chatbot_response(self.client, self.model_name, input_messages)
        final_response = self.postprocess(chatbot_response)
        return final_response

    def postprocess(self, raw_output):
        """
        Parses the raw JSON output from the chatbot and constructs the final response dictionary.
        
        Parameters:
            raw_output (str): Raw JSON string from the chatbot.
        
        Returns:
            dict: Formatted response with role, content, and memory fields.
        """
        try:
            # Print the raw output for debugging
            print("Raw output from model:", raw_output)
            
            # Try to parse the JSON
            parsed_output = json.loads(raw_output)
            
            # Construct the final output dictionary with the expected keys and structure
            formatted_output = {
                "role": "assistant",
                "content": parsed_output.get('message', ''),
                "memory": {
                    "agent": "secure_agent",
                    "guard_decision": parsed_output.get('decision', '')
                }
            }
            return formatted_output
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            # Fallback response for when JSON parsing fails
            return {
                "role": "assistant",
                "content": "Sorry, I encountered an error processing your request.",
                "memory": {
                    "agent": "secure_agent",
                    "guard_decision": "error",
                    "error": str(e)
                }
            }
