from transformers import AutoTokenizer

# https://huggingface.co/docs/transformers/model_doc/gpt2

class AutoTokenizerOptions:
    GPT2 = "gpt2"
    roBERTaSentiment = lambda path: f"{path}/cardiffnlp/twitter-roberta-base-sentiment"
    SalesforceCodeGen2B = "Salesforce/codegen-2B-multi"
    r3dhummingbirdDialoGPT = "r3dhummingbird/DialoGPT-marxbot"

def get_tokenizer(tokenizer_type:str):
    return AutoTokenizer.from_pretrained(tokenizer_type)