from transformers import T5Tokenizer # Tokenizer  
from transformers import T5ForConditionalGeneration # PyTorch model  

TOKEN_NAME = 'unicamp-dl/ptt5-base-portuguese-vocab'
MODEL_NAME = 'phpaiola/ptt5-base-summ-xlsum'

tokenizer = T5Tokenizer.from_pretrained(TOKEN_NAME)
model_pt = T5ForConditionalGeneration.from_pretrained(MODEL_NAME)

def summarize_text(text): 
    inputs = tokenizer.encode(text, max_length=512, truncation=True, return_tensors='pt')
    summary_ids = model_pt.generate(inputs, max_length=256, min_length=32, num_beams=5, no_repeat_ngram_size=3, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0])
    return summary
