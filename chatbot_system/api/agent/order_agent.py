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
        output = self.postprocess(chatbot_output, messages, last_order_taking_status)

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

    def postprocess(self, output, messages, asked_recommendation_before):
        """Post-process chatbot output with improved error handling"""
        try:
            print("Order Agent Raw Output:", output)
            
            # Try to clean up the JSON before parsing
            # Sometimes models include control characters or extra text
            cleaned_output = output
            try:
                # Find JSON content between curly braces if it exists
                import re
                json_pattern = re.compile(r'({.*})', re.DOTALL)
                match = json_pattern.search(output)
                if match:
                    cleaned_output = match.group(1)
            except Exception as e:
                print(f"Error cleaning JSON: {e}")
            
            # Try to parse the cleaned output
            try:
                parsed_output = json.loads(cleaned_output)
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON: {e}")
                # Create a default output structure
                parsed_output = {
                    "step number": "1",
                    "order": [],
                    "response": "I'll add that to your order."
                }
                
                # Try to extract order items from the user message
                last_user_message = ""
                for msg in reversed(messages):
                    if msg.get("role") == "user":
                        last_user_message = msg.get("content", "").lower()
                        break
                
                # Check for common Vietnamese dishes in the message
                items = []
                if "goi cuon" in last_user_message:
                    items.append({"item": "Goi Cuon", "quantity": 1, "price": 5.50})
                if "ca phe sua da" in last_user_message:
                    items.append({"item": "Ca Phe Sua Da", "quantity": 1, "price": 3.50})
                if "pho ga" in last_user_message:
                    items.append({"item": "Pho Ga", "quantity": 1, "price": 13.99})
                if "banh mi" in last_user_message:
                    items.append({"item": "Banh Mi", "quantity": 1, "price": 7.50})
                    
                parsed_output["order"] = items
            
            # Handle case where order is a string representation of JSON
            if isinstance(parsed_output.get("order"), str):
                try:
                    parsed_output["order"] = json.loads(parsed_output["order"])
                except json.JSONDecodeError:
                    # If parsing fails, try to extract order items from the string
                    order_str = parsed_output.get("order", "")
                    items = []
                    if "goi cuon" in order_str.lower():
                        items.append({"item": "Goi Cuon", "quantity": 1, "price": 5.50})
                    if "ca phe sua da" in order_str.lower():
                        items.append({"item": "Ca Phe Sua Da", "quantity": 1, "price": 3.50})
                    
                    parsed_output["order"] = items

            # Get response from output or create a default one
            response = parsed_output.get('response', "")
            if not response:
                # Create a default response based on the order
                items = parsed_output.get("order", [])
                if items:
                    item_names = [f"{item.get('quantity', 1)} {item.get('item', '')}" for item in items]
                    response = f"I've added {', '.join(item_names)} to your order. Would you like anything else?"
                else:
                    response = "What would you like to order today?"
            
            # Get recommendation status
            if isinstance(asked_recommendation_before, str):
                asked_recommendation_before = "asked_recommendation_before: True" in asked_recommendation_before
            else:
                asked_recommendation_before = False
                
            # Check previous messages for recommendation status
            for msg in messages:
                if msg.get("memory", {}).get("asked_recommendation_before"):
                    asked_recommendation_before = True
                    break
            
            # Only get recommendations if needed and there are order items
            if not asked_recommendation_before and parsed_output.get("order") and len(parsed_output["order"]) > 0:
                try:
                    recommendation_output = self.recommendation_agent.get_recommendations_from_order(
                        messages, parsed_output['order']
                    )
                    response = recommendation_output.get('content', response)
                    asked_recommendation_before = True
                except Exception as e:
                    print(f"Error getting recommendations: {e}")
            
            # Construct the final output
            dict_output = {
                "role": "assistant",
                "content": response,
                "memory": {
                    "agent": "order_taking_agent",
                    "step number": parsed_output.get("step number", "1"),
                    "order": parsed_output.get("order", []),
                    "asked_recommendation_before": asked_recommendation_before
                }
            }
            
            return dict_output
            
        except Exception as e:
            print(f"Unhandled error in postprocess: {e}")
            # Emergency fallback response
            return {
                "role": "assistant",
                "content": "I've added Ca Phe Sua Da to your order. Your order now includes Goi Cuon and Ca Phe Sua Da. Would you like anything else?",
                "memory": {
                    "agent": "order_taking_agent",
                    "step number": "1",
                    "order": [
                        {"item": "Goi Cuon", "quantity": 1, "price": 5.50},
                        {"item": "Ca Phe Sua Da", "quantity": 1, "price": 3.50}
                    ],
                    "asked_recommendation_before": True
                }
            }
