
from transformers import AutoTokenizer, MBartForConditionalGeneration

TOKENIZER_NAME = "facebook/mbart-large-cc25"
MODEL_NAME = "GiordanoB/mbart-large-50-finetuned-summarization-V2"

tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_NAME)
model_pt = MBartForConditionalGeneration.from_pretrained(MODEL_NAME)

# from transformers import T5Tokenizer, T5ForConditionalGeneration 
# TOKENIZER_NAME = 'unicamp-dl/ptt5-base-portuguese-vocab'
# MODEL_NAME = 'phpaiola/ptt5-base-summ-xlsum'

def summarize_text(text: str): 
    inputs = tokenizer.encode(text, max_length=512, truncation=True, return_tensors='pt')
    summary_ids = model_pt.generate(inputs, max_length=256, min_length=32, num_beams=5, no_repeat_ngram_size=3)
    summary = tokenizer.decode(summary_ids[0])
    return summary