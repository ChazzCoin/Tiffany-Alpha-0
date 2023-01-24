# from transformers import DPRContextEncoder, DPRContextEncoderTokenizer, DPRQuestionEncoder, AutoTokenizer
#
# model: DPRQuestionEncoder = DPRQuestionEncoder.from_pretrained("vblagoje/dpr-question_encoder-single-lfqa-wiki").to('cpu')
# tokenizer = AutoTokenizer.from_pretrained("vblagoje/dpr-question_encoder-single-lfqa-wiki")
#
# input_ids = tokenizer("Why do airplanes leave contrails in the sky?", return_tensors="pt")["input_ids"]
# embeddings = model(input_ids).pooler_output


from transformers import GPT2Tokenizer, GPT2LMHeadModel

# Load the pre-trained tokenizer and model
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2").to('cpu')

# Encode the input question
input_ids = tokenizer.encode("How many people makes a crowd?", return_tensors="pt")

# Generate a response
response_output = model.generate(input_ids, max_length=100, do_sample=True, top_p=0.95, top_k=40)
response_text = tokenizer.decode(response_output[0], skip_special_tokens=True)
print(response_text)



# response_model = DPRContextEncoder.from_pretrained("vblagoje/dpr-context_encoder-single-nq-wiki").to('cpu')
# response_tokenizer = AutoTokenizer.from_pretrained("vblagoje/dpr-context_encoder-single-nq-wiki")
#
# response_input_ids = tokenizer.encode(embeddings, return_tensors="pt")
# response_output = response_model.generate(response_input_ids, max_length=100, do_sample=True)
# response_text = tokenizer.decode(response_output, skip_special_tokens=True)
# print(response_text)