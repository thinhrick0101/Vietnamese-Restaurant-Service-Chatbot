from agent import secure_agent, classification_agent, details_agent, order_agent, recommendation_agent, AgentProtocol
import os

def main():
    # guard_agent = secure_agent.SecureAgent()
    # classification_agent = classification_agent.ClassificationAgent()
    # recommendation_agent = RecommendationAgent('recommendation_objects/apriori_recommendations.json',
    #                                                 'recommendation_objects/popularity_recommendation.csv'
    #                                                 )
    # agent_dict: dict[str, AgentProtocol] = {
    #     "details_agent": DetailsAgent(),
    #     "order_taking_agent": OrderTakingAgent(recommendation_agent),
    #     "recommendation_agent": recommendation_agent
    # }
    
    # messages = []
    # while True:
    #     # Display the chat history
    #     os.system('cls' if os.name == 'nt' else 'clear')
        
    #     print("\n\nPrint Messages ...............")
    #     for message in messages:
    #         print(f"{message['role'].capitalize()}: {message['content']}")

    #     # Get user input
    #     prompt = input("User: ")
    #     messages.append({"role": "user", "content": prompt})

    #     # Get GuardAgent's response
    #     guard_agent_response = guard_agent.get_response(messages)
    #     if guard_agent_response["memory"]["guard_decision"] == "not allowed":
    #         messages.append(guard_agent_response)
    #         continue
        
    #     # Get ClassificationAgent's response
    #     classification_agent_response = classification_agent.get_response(messages)
    #     chosen_agent=classification_agent_response["memory"]["classification_decision"]
    #     print("Chosen Agent: ", chosen_agent)

    #     # Get the chosen agent's response
    #     agent = agent_dict[chosen_agent]
    #     response = agent.get_response(messages)
        
    #     messages.append(response)
    pass
        
        

if __name__ == "__main__":
    guard_agent = secure_agent.SecureAgent()
    classification_agent = classification_agent.ClassificationAgent()
    recommendation_agent = recommendation_agent.RecommendationAgent('fav_foods/recommendations.json',
                                                                        'fav_foods/recommended_products.csv'
                                                                        )
    messages =[]
    agent_dict: dict[str, AgentProtocol] = {
        "details_agent": details_agent.DetailsAgent(),
        "recommendation_agent": recommendation_agent,
        "order_agent": order_agent.OrderTakingAgent(recommendation_agent)
                                                                        
    }
    # recommendation_agent= recommendation_agent.RecommendationAgent('fav_foods/recommendations.json',
    #                                                     'fav_foods/recommended_products.csv'
    #                                                     )
    # print(recommendation_agent._get_apriori_recommendations(['Banh Khot']))

    while True:
        # os.system('cls' if os.name == 'nt' else 'clear')
        print('\n\nPrint Messages ...............')
        for message in messages:
            print(f"{message['role'].capitalize()}: {message['content']}")
        prompt = input("User: ")
        messages.append({"role": "user", "content": prompt})
        guard_agent_response = guard_agent.get_response(messages)
        if guard_agent_response["memory"]["guard_decision"] == "not allowed":
            messages.append(guard_agent_response)
            continue
        classification_agent_response = classification_agent.get_response(messages)
        chosen_agent=classification_agent_response["memory"]["classification_decision"]
        print("Chosen Agent: ", chosen_agent)

        agent = agent_dict[chosen_agent]
        response = agent.get_response(messages)
        messages.append(response)
        