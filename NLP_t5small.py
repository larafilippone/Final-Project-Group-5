from transformers import T5Tokenizer, T5ForConditionalGeneration

# Initialize the tokenizer and model
tokenizer = T5Tokenizer.from_pretrained('t5-small')
model = T5ForConditionalGeneration.from_pretrained('t5-small')

# Define a function to summarize reviews
def summarize_review(review_text: str) -> str:
    inputs = tokenizer.encode("summarize: " + review_text, return_tensors="pt", max_length=512, truncation=True)
    summary_ids = model.generate(inputs, max_length=20, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

# Example usage:
if __name__ == '__main__':
    # Assuming you have fetched a review in `review_text`
    for review in all_results:
        summary = summarize_review(review['review_text'])
        print(summary)