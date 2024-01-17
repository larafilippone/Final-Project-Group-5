import openai

def ask_chatgpt(request_summary):

    # Set your OpenAI API key
    openai.api_key = "xxx"

    # Create chat completions using the OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an informative assistant."},
            {"role": "user", "content": request_summary},
        ],
        temperature=0.7,
    )

    # Access the generated content
    generated_content = response['choices'][0]['message']['content']
    return generated_content.strip()

