from transformers import AutoTokenizer, MBartForConditionalGeneration
import re

TOKENIZER_NAME = "facebook/mbart-large-cc25"
MODEL_NAME = "GiordanoB/mbart-large-50-finetuned-summarization-V2"
TAG_CLEANER = re.compile('<.*?>') 


print("Loading in models for summarization...")
tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_NAME)
model_pt = MBartForConditionalGeneration.from_pretrained(MODEL_NAME)
print("Models loaded successfully!")


# from transformers import T5Tokenizer, T5ForConditionalGeneration 
# TOKENIZER_NAME = 'unicamp-dl/ptt5-base-portuguese-vocab'
# MODEL_NAME = 'phpaiola/ptt5-base-summ-xlsum'

def summarize_text(text: str): 
    inputs = tokenizer.encode(text, max_length=512, truncation=True, return_tensors='pt')
    summary_ids = model_pt.generate(inputs, max_length=256, min_length=32, num_beams=5, no_repeat_ngram_size=3)
    summary = tokenizer.decode(summary_ids[0])

    return _sanitize_summ(summary)


def _sanitize_summ(text: str) -> str:
    # Cleans the tags that the model for some god forsaken reason appends to the output
    clean_text = re.sub(TAG_CLEANER, '', text).strip()
    # Capitalize the first letter  
    clean_text = clean_text[0].upper() + clean_text[1:]

    return clean_text