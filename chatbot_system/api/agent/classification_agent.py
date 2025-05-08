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
            You are a helpful AI assistant for a coffee shop application.
            Your task is to determine what agent should handle the user input. You have 3 agents to choose from:
            1. details_agent: This agent is responsible for answering questions about the coffee shop, like location, delivery places, working hours, details about menue items. Or listing items in the menu items. Or by asking what we have.
            2. order_agent: This agent is responsible for taking orders from the user. It's responsible to have a conversation with the user about the order untill it's complete.
            3. recommendation_agent: This agent is responsible for giving recommendations to the user about what to buy. If the user asks for a recommendation, this agent should be used.

            Your output should be in a structured json format like so. each key is a string and each value is a string. Make sure to follow the format exactly:
            {
            "chain of thought": go over each of the agents above and write some your thoughts about what agent is this input relevant to.
            "decision": "details_agent" or "order_taking_agent" or "recommendation_agent". Pick one of those. and only write the word.
            "message": leave the message empty.
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
