import os
from dotenv import load_dotenv
from openai import OpenAI
from .utils import get_chatbot_response, get_embedding
from pinecone import Pinecone
from copy import deepcopy

load_dotenv()


class DetailsAgent:
    def __init__(self):
        # Initialize clients for OpenAI and Pinecone
        self.client = OpenAI(
            api_key=os.getenv("RUNPOD_TOKEN"),
            base_url=os.getenv("RUNPOD_CHATBOT_URL"),
        )
        self.embedding_client = OpenAI(
            api_key=os.getenv("RUNPOD_TOKEN"), 
            base_url=os.getenv("RUNPOD_EMBEDDING_URL")
        )
        self.model_name = os.getenv("MODEL_NAME")
        self.pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        self.index_name = os.getenv("PINECONE_INDEX_NAME")

    def get_closest_results(self, index_name, input_embeddings, top_k=2):
        """Fetch the closest results from Pinecone index based on the embedding."""
        index = self.pc.Index(index_name)
        
        results = index.query(
            namespace="ns1",
            vector=input_embeddings,
            top_k=top_k,
            include_values=False,
            include_metadata=True
        )
        return results

    def get_response(self, messages):
        """Generate a response based on user query using Pinecone and OpenAI."""
        messages = deepcopy(messages)

        user_message = messages[-1]['content']
        
        # Get embedding for the user message
        embedding = get_embedding(self.embedding_client, self.model_name, user_message)[0]
        
        # Retrieve closest matching knowledge from Pinecone
        result = self.get_closest_results(self.index_name, embedding)
        
        # Prepare the source knowledge from the retrieved matches
        source_knowledge = "\n".join([x['metadata']['text'].strip() for x in result['matches']])

        # Construct the prompt for the chatbot
        prompt = f"""
        Using the contexts below, answer the query.

        Contexts:
        {source_knowledge}

        Query: {user_message}
        """

        # System prompt specifying the assistant's role
        system_prompt = """
        You are a customer support agent for a restaurant called Mrs.Phuong Cozzy. 
        You should answer every question as if you are a waiter and provide necessary information to the user regarding their orders.
        """

        # Append the system prompt and the user query to the messages
        messages[-1]['content'] = prompt
        input_messages = [{"role": "system", "content": system_prompt}] + messages[-3:]

        # Get chatbot response
        chatbot_output = get_chatbot_response(self.client, self.model_name, input_messages)

        # Post-process the chatbot output
        output = self.postprocess(chatbot_output)

        return output

    def postprocess(self, output):
        """Post-process the response from the chatbot."""
        # Wrapping the chatbot output in a structured response
        return {
            "role": "assistant",
            "content": output,
            "memory": {"agent": "details_agent"}
        }
