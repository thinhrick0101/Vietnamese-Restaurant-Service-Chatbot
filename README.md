# Vietnamese Restaurant Service Chatbot

## Project Overview
The Vietnamese Restaurant Service Chatbot is designed to assist customers in exploring and ordering from a Vietnamese restaurant's menu. It leverages machine learning models to provide personalized recommendations based on user preferences and past interactions.

## Features
- **Menu Exploration**: Browse through a detailed menu of Vietnamese dishes.
- **Personalized Recommendations**: Get dish recommendations based on your preferences.
- **Order Placement**: Place orders directly through the chatbot.
- **Nutritional Information**: Access detailed nutritional information for each dish.
- **Customer Feedback**: Provide feedback on dishes and service.

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/vietnamese-restaurant-chatbot.git
    cd vietnamese-restaurant-chatbot
    ```

2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up environment variables:
    Create a `.env` file in the root directory and add the necessary environment variables:
    ```env
    OPENAI_API_KEY=your_openai_api_key
    FIREBASE_API_KEY=your_firebase_api_key
    ```

### Running the Application
1. Start the server:
    ```bash
    python e:\Project\Vietnamese Restaurant Service Chatbot\chatbot_system\api\main.py
    ```

2. Access the chatbot through the provided endpoint.

## Project Structure
- `chatbot_system/`: Contains the main chatbot logic and machine learning models.
- `products/`: Contains product details and images.
- `requirements.txt`: Lists all the dependencies required for the project.
- `.env`: Environment variables for API keys and other configurations.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License.
