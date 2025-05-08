from agent import (SecuredAgent,
                    ClassificationAgent,
                    DetailsAgent,
                    OrderTakingAgent,
                    RecommendationAgent,
                    AgentProtocol
                    )

class BrainAgent():
    def __init__(self):
        self.guard_agent = SecuredAgent()
        self.classification_agent = ClassificationAgent()
        
        # Create a recommendation agent
        rec_agent = RecommendationAgent(
            'fav_foods/recommendations.json',
            'fav_foods/recommended_products.csv'
        )
        
        # Create the agent dictionary with the correct keys
        self.agent_dict: dict[str, AgentProtocol] = {
            "details_agent": DetailsAgent(),
            "recommendation_agent": rec_agent,
            "order_taking_agent": OrderTakingAgent(rec_agent)
        }
    
    def get_response(self, job):
        # Extract messages from job input
        messages = job["input"]["messages"]
        
        # Get guard agent response
        guard_agent_response = self.guard_agent.get_response(messages)
        
        # If guard agent decides to block the request, return its response
        if guard_agent_response["memory"]["guard_decision"] != "allowed":
            return {"output": guard_agent_response}
        
        # Get classification agent response to determine which agent to use
        classification_agent_response = self.classification_agent.get_response(messages)
        chosen_agent = classification_agent_response["memory"]["classification_decision"]
        
        # Map the agent name to the correct key if needed
        agent_key_mapping = {
            "order_agent": "order_taking_agent",  # Map order_agent to order_taking_agent
            "details_agent": "details_agent",
            "recommendation_agent": "recommendation_agent"
        }
        
        # Get the correct agent key
        agent_key = agent_key_mapping.get(chosen_agent, chosen_agent)
        
        # Check if the agent key exists in the dictionary
        if agent_key not in self.agent_dict:
            print(f"Warning: Agent '{chosen_agent}' (mapped to '{agent_key}') not found in agent_dict")
            print(f"Available agents: {list(self.agent_dict.keys())}")
            # Default to details_agent if the requested agent doesn't exist
            agent_key = "details_agent"
        
        # Get the agent
        agent = self.agent_dict[agent_key]
        
        # Get response from the chosen agent
        agent_response = agent.get_response(messages)
        
        # Return the response
        return {"output": agent_response}