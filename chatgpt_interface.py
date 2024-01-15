import openai

# Set your OpenAI API key
openai.api_key = "xxx"

def ask_chatgpt(question):
    # Create chat completions using the OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an informative assistant."},
            {"role": "user", "content": f"Ask ChatGPT: {question}"},
        ],
        temperature=0.7,
        max_tokens=100,
    )

    # Access the generated content
    generated_content = response['choices'][0]['message']['content']
    return generated_content.strip()

# Ask a question
user_question = input("Ask ChatGPT: ")
answer = ask_chatgpt(user_question)

# Display the answer
print(f"ChatGPT's Answer: {answer}")