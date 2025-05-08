from agent.secure_agent import SecureAgent as SecuredAgent
from agent.classification_agent import ClassificationAgent
from agent.details_agent import DetailsAgent
from agent.order_agent import OrderTakingAgent
from agent.recommendation_agent import RecommendationAgent
from agent.utils import get_chatbot_response, double_check_json_output

# Protocol class for type checking
class AgentProtocol:
    def get_response(self, messages):
        pass

