from transformers import AutoTokenizer, AutoModelForCausalLM
tokenizer = AutoTokenizer.from_pretrained("Salesforce/codegen-2B-multi") # 16B, 6B, 2B,
model = AutoModelForCausalLM.from_pretrained("Salesforce/codegen-2B-multi")

text = "create python merge sort function"
input_ids = tokenizer(text, return_tensors="pt").input_ids

generated_ids = model.generate(input_ids, max_length=128)
print(tokenizer.decode(generated_ids[0], skip_special_tokens=True))