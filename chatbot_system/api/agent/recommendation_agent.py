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
            if recommendation['product'] not in unique_recommendations:
                category = recommendation['product_category']
                category_count[category] = category_count.get(category, 0)

                # Limit to 2 recommendations per category
                if category_count[category] < 2:
                    unique_recommendations.append(recommendation['product'])
                    category_count[category] += 1

                if len(unique_recommendations) >= top_k:
                    break

        return unique_recommendations

    def _get_popular_recommendations(self, product_categories=None, top_k=5):
        recommendations_df = self.popular_recommendations

        if product_categories:
            if isinstance(product_categories, str):
                product_categories = [product_categories]
            recommendations_df = recommendations_df[recommendations_df['product_category'].isin(product_categories)]

        recommendations_df = recommendations_df.sort_values(by='number_of_transactions', ascending=False)

        return recommendations_df['product'].tolist()[:top_k] if recommendations_df.shape[0] > 0 else []

    def _recommendation_classification(self, messages):
        system_prompt = f"""
        You are a helpful AI assistant for a restaurant application which serves food, drinks and pastries. 
        We have 3 types of recommendations:

        1. Apriori Recommendations: These are based on the user's order history.
        2. Popular Recommendations: These are based on the most popular items in the shop.
        3. Popular Recommendations by Category: Recommendations based on a product category.

        Available items in the restaurant:
        {", ".join(self.products)}

        Available categories:
        {", ".join(self.product_categories)}

        Your task is to determine which type of recommendation to provide based on the user's message.

        Your output should be a JSON with the format:
        {{
            "chain of thought": "Explain your reasoning here.",
            "recommendation_type": "apriori" or "popular" or "popular by category",
            "parameters": List of items or categories based on recommendation type.
        }}
        """

        input_messages = [{"role": "system", "content": system_prompt}] + messages[-3:]
        chatbot_output = get_chatbot_response(self.client, self.model_name, input_messages)
        return self._postprocess_classification(chatbot_output)

    def get_response(self, messages):
        classification = self._recommendation_classification(messages)
        recommendation_type = classification['recommendation_type']
        recommendations = []

        if recommendation_type == "apriori":
            recommendations = self._get_apriori_recommendations(classification['parameters'])
        elif recommendation_type == "popular":
            recommendations = self._get_popular_recommendations()
        elif recommendation_type == "popular by category":
            recommendations = self._get_popular_recommendations(classification['parameters'])

        if not recommendations:
            return {"role": "assistant", "content": "Sorry, I can't help with that. Can I assist you with your order?"}

        recommendations_str = ", ".join(recommendations)
        system_prompt = f"""
        You are a helpful assistant for a restaurant.
        Please recommend the following items to the user:
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

    def _postprocess_classification(self, output):
        output = json.loads(output)
        return {
            "recommendation_type": output['recommendation_type'],
            "parameters": output['parameters'],
        }

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
