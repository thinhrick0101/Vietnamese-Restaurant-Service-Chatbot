import os
import json
from dotenv import load_dotenv
from copy import deepcopy
from .utils import get_chatbot_response
from openai import OpenAI

load_dotenv()


class ClassificationAgent:
    def __init__(self):
        # Initialize OpenAI client and model configuration
        self.client = OpenAI(
            api_key=os.getenv("RUNPOD_TOKEN"),
            base_url=os.getenv("RUNPOD_CHATBOT_URL"),
        )
        self.model_name = os.getenv("MODEL_NAME")

    def get_response(self, messages):
        """Determine which agent should handle the user input."""
        messages = deepcopy(messages)

        # Define the system-level prompt that guides the classification
        system_prompt = """
        You are a helpful AI assistant for a restaurant application.
        Your task is to determine what agent should handle the user input. You have 3 agents to choose from:
        1. details_agent: This agent answers questions about the restaurant, such as location, delivery options, working hours, details about menu items, or asking what is available.
        2. order_taking_agent: This agent handles the process of taking an order, engaging in conversation with the user until the order is complete.
        3. recommendation_agent: This agent provides recommendations to users about what to purchase when asked.

        Your output should be structured as follows:
        {
            "chain of thought": "Go over each agent and reason which one fits the input.",
            "decision": "details_agent" or "order_taking_agent" or "recommendation_agent",
            "message": "Leave the message empty."
        }
        """

        # Create the message history with the system prompt followed by the last few user inputs
        input_messages = [{"role": "system", "content": system_prompt}]
        input_messages += messages[-3:]

        # Get the chatbot's classification decision
        chatbot_output = get_chatbot_response(self.client, self.model_name, input_messages)

        # Post-process the chatbot output
        output = self.postprocess(chatbot_output)

        return output

    def postprocess(self, output):
        """Post-process the chatbot's response into the desired output format."""
        output = json.loads(output)

        # Construct the response with the agent classification decision
        dict_output = {
            "role": "assistant",
            "content": output.get('message', ''),
            "memory": {
                "agent": "classification_agent",
                "classification_decision": output.get('decision')
            }
        }
        return dict_output
