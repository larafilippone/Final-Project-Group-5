"""
chatgpt_integration.py: This script manages the integration with the ChatGPT API. 
It includes functions to send requests and process responses from the ChatGPT service for generating summaries and suggestions.
"""

import openai

# Create a function to access the OpenAI API and return the answer from Chat GPT
def ask_chatgpt(question_to_chatgpt: str) -> str:
    """
    Accesses the API of Chat GPT and returns the generated content 

    Arguments:
    question_to_chatgpt (str): the input question for chat GPT

    Returns:
    generated_content (str): a string containing the content generated by chat GPT 
    """

    # error handling 
    try:
        # Insert the key for Open AI 
        openai.api_key = "xx"

        # Accesses the API of Chat GPT to ask the question_to_chatgpt generated earlier 
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an informative assistant."},
                {"role": "user", "content": question_to_chatgpt},
            ],
            temperature=0.7,
        )

        # Save and return the generated content
        generated_content = response['choices'][0]['message']['content']

        return str(generated_content.strip())

    except openai.error.AuthenticationError as e:
        print(f"OpenAI API error: {e}")
        return "Authentication error: please check your Chat GPT API key"
    except ValueError as ve:
        print(f"Value error: {ve}")
        return "A value error occurred while processing your request."
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")
        return "An unexpected error occurred while processing your request."