def get_chatbot_response(client, model_name, messages, temperature=0):
    """
    Generates a chatbot response based on the given messages.

    Args:
        client: OpenAI client instance.
        model_name (str): The model to be used for generating responses.
        messages (list): List of message dictionaries with "role" and "content".
        temperature (float, optional): Controls randomness of responses. Default is 0.

    Returns:
        str: The chatbot's response.
    """
    input_messages = [{"role": msg["role"], "content": msg["content"]} for msg in messages]

    response = client.chat.completions.create(
        model=model_name,
        messages=input_messages,
        temperature=temperature,
        top_p=0.8,
        max_tokens=2000,
    )

    return response.choices[0].message.content


def get_embedding(embedding_client, model_name, text_input):
    """
    Generates embeddings for the given text input.

    Args:
        embedding_client: OpenAI embedding client instance.
        model_name (str): The embedding model to be used.
        text_input (str): The text to generate embeddings for.

    Returns:
        list: A list of embedding vectors.
    """
    output = embedding_client.embeddings.create(input=text_input, model=model_name)

    return [embedding_object.embedding for embedding_object in output.data]


def double_check_json_output(client, model_name, json_string):
    """
    Validates and corrects a JSON string.

    Args:
        client: OpenAI client instance.
        model_name (str): The model used for validation.
        json_string (str): The JSON string to be checked.

    Returns:
        str: The corrected JSON string.
    """
    prompt = (
        f"You will check this JSON string and correct any mistakes that make it invalid. "
        f"Then you will return the corrected JSON string. Nothing else. "
        f"If the JSON is correct, just return it.\n\n"
        f"Do NOT return a single letter outside of the JSON string.\n\n"
        f"{json_string}"
    )

    messages = [{"role": "user", "content": prompt}]
    return get_chatbot_response(client, model_name, messages)
