import torch
from transformers import DistilBertTokenizer, DistilBertForQuestionAnswering

# Load the pre-trained tokenizer and model
tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-cased-distilled-squad")
model = DistilBertForQuestionAnswering.from_pretrained("distilbert-base-cased-distilled-squad").to('cpu')

# Encode the input question and context
input_text = "Why do airplanes leave contrails in the sky?"
input_ids = tokenizer.encode(input_text, return_tensors="pt")

# Generate a response
response = model(input_ids)
answer_start_scores, answer_end_scores = response.start_logits, response.end_logits
answer_start = torch.argmax(answer_start_scores)
answer_end = torch.argmax(answer_end_scores)
response_text = tokenizer.decode(input_ids[0][answer_start:answer_end+1], skip_special_tokens=True)
print(response_text)