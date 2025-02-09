import os
import json
from .utils import get_chatbot_response, double_check_json_output
from openai import OpenAI
from copy import deepcopy
from dotenv import load_dotenv

load_dotenv()


class OrderTakingAgent:
    def __init__(self, recommendation_agent):
        self.client = OpenAI(
            api_key=os.getenv("RUNPOD_TOKEN"),
            base_url=os.getenv("RUNPOD_CHATBOT_URL"),
        )
        self.model_name = os.getenv("MODEL_NAME")
        self.recommendation_agent = recommendation_agent

    def get_response(self, messages):
        messages = deepcopy(messages)

        # Prepare the system prompt with the coffee shop menu and guidelines
        system_prompt = """
            You are a customer support Bot for a restaurant called "Mrs.Phuong Cozzy".
            
            Here is the menu:
            - Pho Ga - $6.50
            - Goi Cuon - $5.00
            - Hu Tieu Nam Vang - $7.00
            - Tra Da - $1.50
            - Nuoc Mia - $2.00
            - Banh Xeo - $6.00
            - Ca Phe Sua Da - $3.50
            - Banh Mi Thit - $4.50
            - Banh Trang Nuong - $2.50
            - Xoi Ga - $5.00
            - Bun Rieu - $6.00
            - Goi Ga - $4.50
            - Banh Pia - $2.50
            - Bun Cha - $7.50
            - Kem Xoi - $4.00
            - Bun Dau Mam Tom - $5.50
            - Bun Oc - $6.50
            - Banh Beo - $3.50
            - Nuoc Chanh - $2.00
            - Nem Nuong - $4.00
            - Banh Mi Cha Ca - $4.50
            - Banh Khot - $3.50
            - Sinh To Bo - $3.00
            - Bun Thit Nuong - $7.00
            - Com Ga - $6.50
            - Lau Nam - $9.00
            - Che Troi Nuoc - $3.00
            - Sinh To Xoai - $3.50
            - Com Tam - $5.50
            - Che Ba Mau - $3.00
            - Bo Nuong La Lot - $8.00
            
            Things to NOT DO:
            * Don’t ask about payment methods (cash/card).
            * Don’t tell the user to go to the counter.
            * Don’t ask the user to go somewhere to pick up the order.
            
            Your task:
            1. Take the user's order.
            2. Validate that all items are on the menu.
            3. If an item is missing, inform the user and repeat the valid items.
            4. Ask if they need anything else.
            5. If yes, repeat the process.
            6. If no, summarize the order, including item names, prices, and the total.
            
            The user message will contain "order" and "step number" in the memory section.
            
            Your output should follow this exact format:
            {
                "chain of thought": "Explanation of the current step and reasoning.",
                "step number": "Determine the current task number.",
                "order": [{"item": "<item name>", "quantity": <quantity>, "price": <price>}],
                "response": "Your response to the user."
            }
        """

        # Retrieve the previous order status from the conversation memory
        last_order_taking_status = self._get_last_order_status(messages)

        # Prepare the conversation for the chatbot
        messages[-1]['content'] = last_order_taking_status + " \n " + messages[-1]['content']
        input_messages = [{"role": "system", "content": system_prompt}] + messages

        # Get the chatbot response
        chatbot_output = get_chatbot_response(self.client, self.model_name, input_messages)

        # Double-check the JSON output
        chatbot_output = double_check_json_output(self.client, self.model_name, chatbot_output)

        # Post-process the chatbot response
        output = self._postprocess(chatbot_output, messages, last_order_taking_status)

        return output

    def _get_last_order_status(self, messages):
        """Extract the last order status from the conversation memory."""
        for message_index in range(len(messages) - 1, 0, -1):
            message = messages[message_index]
            agent_name = message.get("memory", {}).get("agent", "")
            if message["role"] == "assistant" and agent_name == "order_taking_agent":
                step_number = message["memory"]["step number"]
                order = message["memory"]["order"]
                asked_recommendation_before = message["memory"]["asked_recommendation_before"]
                return f"step number: {step_number}\norder: {order}"

        return ""

    def _postprocess(self, output, messages, last_order_taking_status):
        """Post-process the chatbot's output and integrate it with the order-taking logic."""
        output = json.loads(output)

        # Ensure that the order is in the correct format
        if isinstance(output["order"], str):
            output["order"] = json.loads(output["order"])

        response = output['response']

        # Provide recommendations if the user hasn't received any yet
        if not output.get("asked_recommendation_before", False) and len(output["order"]) > 0:
            recommendation_output = self.recommendation_agent.get_recommendations_from_order(messages, output['order'])
            response = recommendation_output['content']
            output["asked_recommendation_before"] = True

        # Return the final response with memory
        return {
            "role": "assistant",
            "content": response,
            "memory": {
                "agent": "order_taking_agent",
                "step number": output["step number"],
                "order": output["order"],
                "asked_recommendation_before": output["asked_recommendation_before"]
            }
        }
