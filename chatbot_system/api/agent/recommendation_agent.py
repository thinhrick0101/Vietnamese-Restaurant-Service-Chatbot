import json
import pandas as pd
import os
from .utils import get_chatbot_response
from openai import OpenAI
from copy import deepcopy
from dotenv import load_dotenv
load_dotenv()


class RecommendationAgent:
    def __init__(self, apriori_recommendation_path, popular_recommendation_path):
        self.client = OpenAI(
            api_key=os.getenv("RUNPOD_TOKEN"),
            base_url=os.getenv("RUNPOD_CHATBOT_URL"),
        )
        self.model_name = os.getenv("MODEL_NAME")

        with open(apriori_recommendation_path, 'r') as file:
            self.apriori_recommendations = json.load(file)

        self.popular_recommendations = pd.read_csv(popular_recommendation_path)
        self.products = self.popular_recommendations['product'].tolist()
        self.product_categories = self.popular_recommendations['product_category'].tolist()

    def _get_apriori_recommendations(self, products, top_k=5):
        recommendations = []
        category_count = {}

        for product in products:
            if product in self.apriori_recommendations:
                recommendations += self.apriori_recommendations[product]

        # Sort recommendations by confidence
        recommendations = sorted(recommendations, key=lambda x: x['confidence'], reverse=True)

        unique_recommendations = []
        for recommendation in recommendations:
            # First check if the product isn't already in our recommendations
            if recommendation['product'] not in unique_recommendations:
                # Check if product_category exists in the recommendation dict
                if 'product_category' in recommendation:
                    category = recommendation['product_category']
                    category_count[category] = category_count.get(category, 0)

                    # Limit to 2 recommendations per category
                    if category_count[category] < 2:
                        unique_recommendations.append(recommendation['product'])
                        category_count[category] += 1
                else:
                    # If no category is provided, just add the product
                    unique_recommendations.append(recommendation['product'])

                # Break if we have enough recommendations
                if len(unique_recommendations) >= top_k:
                    break

        # If we don't have enough recommendations, add popular ones
        if len(unique_recommendations) < top_k:
            popular_products = self._get_popular_recommendations(top_k=top_k-len(unique_recommendations))
            for product in popular_products:
                if product not in unique_recommendations:
                    unique_recommendations.append(product)
                    if len(unique_recommendations) >= top_k:
                        break

        return unique_recommendations

    def _get_popular_recommendations(self, top_k=5):
        """
        Get the most popular items.
        """
        try:
            # Check if the recommendations_df exists and has the required columns
            if hasattr(self, 'recommendations_df') and not self.recommendations_df.empty:
                # Check column names for sorting
                sort_column = None
                if 'number_of_transactions' in self.recommendations_df.columns:
                    sort_column = 'number_of_transactions'
                elif 'count' in self.recommendations_df.columns:
                    sort_column = 'count'
                elif 'popularity' in self.recommendations_df.columns:
                    sort_column = 'popularity'
                
                # If a valid sort column exists, sort by it
                if sort_column:
                    recommendations_df = self.recommendations_df.sort_values(by=sort_column, ascending=False)
                    # Get the top k products
                    return recommendations_df['product'].iloc[:top_k].tolist()
                
            # Fallback to a hardcoded list of popular items if sorting fails
            return ["Pho Ga", "Banh Mi Thit", "Goi Cuon", "Ca Phe Sua Da", "Banh Xeo"][:top_k]
        
        except Exception as e:
            print(f"Error getting popular recommendations: {e}")
            # Return a default list of popular items
            return ["Pho Ga", "Banh Mi Thit", "Goi Cuon", "Ca Phe Sua Da", "Banh Xeo"][:top_k]

    def _recommendation_classification(self, messages):
        """
        Classify the user's recommendation request.
        """
        # Get the most recent user message
        user_message = ""
        for message in reversed(messages):
            if message["role"] == "user":
                user_message = message["content"]
                break
        
        # Define the system prompt
        system_prompt = """
        You are a restaurant assistant helping to classify customer recommendation requests.
        
        Based on the user's message, determine:
        1. Whether they're asking for general recommendations or specific category recommendations
        2. If specific, identify which food categories they're interested in
        
        Respond with ONLY a JSON object in this exact format:
        {
            "classification": "general" or "specific",
            "categories": [] (empty array for general, or array of category names for specific)
        }
        
        Example 1:
        User: "What do you recommend?"
        Response: {"classification": "general", "categories": []}
        
        Example 2:
        User: "What soups do you recommend?"
        Response: {"classification": "specific", "categories": ["soup"]}
        """
        
        # Create the message history with the system prompt and user message
        input_messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
        
        # Get the chatbot's output
        chatbot_output = get_chatbot_response(self.client, self.model_name, input_messages)
        
        # Post-process the classification output
        return self._postprocess_classification(chatbot_output)

    def get_response(self, messages):
        """
        Generate a recommendation response based on the conversation history.
        """
        try:
            # Classify the recommendation request
            classification = self._recommendation_classification(messages)
            
            # Get the most recent user message
            user_message = ""
            for message in reversed(messages):
                if message["role"] == "user":
                    user_message = message["content"]
                    break
            
            # Base system prompt
            system_prompt = """
            You are a restaurant assistant providing recommendations for a Vietnamese restaurant.
            
            Our most popular dishes include:
            - Pho Bo (Beef Noodle Soup)
            - Banh Mi (Vietnamese Sandwich)
            - Goi Cuon (Fresh Spring Rolls)
            - Bun Cha (Grilled Pork with Noodles)
            - Cha Gio (Fried Spring Rolls)
            
            Recommend items the customer might enjoy based on their query.
            Be enthusiastic but concise in your recommendations.
            """
            
            # Add category-specific recommendations if applicable
            if classification.get("classification") == "specific" and classification.get("categories"):
                categories = classification.get("categories", [])
                if "soup" in categories:
                    system_prompt += "\nFor soup dishes, I especially recommend our Pho Bo or Pho Ga."
                if "sandwich" in categories:
                    system_prompt += "\nFor sandwiches, our Banh Mi with grilled pork is exceptional."
                if "appetizer" in categories:
                    system_prompt += "\nFor appetizers, try our Goi Cuon or Cha Gio."
            
            # Create the message history with the system prompt and user message
            input_messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
            
            # Get the chatbot's recommendation
            response = get_chatbot_response(self.client, self.model_name, input_messages)
            
            # Format the final response
            formatted_response = {
                "role": "assistant",
                "content": response,
                "memory": {
                    "agent": "recommendation_agent"
                }
            }
            
            return formatted_response
            
        except Exception as e:
            print(f"Error in recommendation agent: {e}")
            # Provide a fallback response
            return {
                "role": "assistant",
                "content": "I'd recommend trying our signature Pho Bo or Banh Mi. Both are delicious customer favorites!",
                "memory": {
                    "agent": "recommendation_agent",
                    "error": str(e)
                }
            }

    def _postprocess_classification(self, output):
        """
        Post-process the chatbot's output into the desired classification format.
        """
        try:
            # Print raw output for debugging
            print("Recommendation Classification Raw Output:", output)
            
            # Parse the JSON output
            parsed_output = json.loads(output)
            return parsed_output
        except json.JSONDecodeError as e:
            print(f"JSON decode error in recommendation classification: {e}")
            print(f"Raw output: {output}")
            
            # Provide a default classification if parsing fails
            default_classification = {
                "classification": "general",
                "categories": []
            }
            return default_classification

    def get_recommendations_from_order(self, messages, order):
        products = [product['item'] for product in order]
        recommendations = self._get_apriori_recommendations(products)

        recommendations_str = ", ".join(recommendations)
        system_prompt = f"""
        You are a helpful assistant for a restaurant.
        Please recommend the following items to the user based on their order:
        {recommendations_str}
        """

        prompt = f"""
        {messages[-1]['content']}
        Recommend these items: {recommendations_str}
        """
        messages[-1]['content'] = prompt

        input_messages = [{"role": "system", "content": system_prompt}] + messages[-3:]
        chatbot_output = get_chatbot_response(self.client, self.model_name, input_messages)
        return self._postprocess(chatbot_output)

    def _postprocess(self, output):
        return {
            "role": "assistant",
            "content": output,
            "memory": {"agent": "recommendation_agent"}
        }
