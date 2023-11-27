import replicate
import asyncio
import nltk
from math import floor
from multi_rake import Rake

# # Uncomment if nltk whines about not having them
# nltk.download('punkt', quiet=True)
# nltk.download('averaged_perceptron_tagger', quiet=True)

# Consts for analising text
SENTENCE_PARAGRAPH_RATIO = 4
TOOLTIPS_PER_PARAGRAPH = 1
MIN_KW_RATING = 4

# If False call the replicate API, returns a placeholder otherwise.
API_FAILSAFE = True

# User passes a list of concepts, and we return a text explaining them
async def classify_from_concept(concepts: list[str]):
    return await concepts, _async_generate_all(concepts)

# User passes a text, and we return a text explaining the core concepts of it
async def classify_from_text(text: str):
    # Guesses the number of paragraphs in the text with the # of sentences
    sent_num = len(nltk.sent_tokenize(text))
    para_ratio = floor(sent_num / SENTENCE_PARAGRAPH_RATIO)
    para_ratio = para_ratio if para_ratio > 0 else 1 

    # Get how many tooltips we're gonna generate
    tooltip_ratio = para_ratio * TOOLTIPS_PER_PARAGRAPH

    prompts = _get_prompts(text, tooltip_ratio)
    return await classify_from_concept(prompts)

# Async middle man for generating the tooltips
async def _async_generate(concept: str) -> str:
    return { 
        "concept": concept,
        "tooltip":  _generate_tooltip(concept) 
        } 

# Create all the parallel task to do asynchronously
async def _async_generate_all(concepts: list[str]) -> list[str]:
    tasks = []
    # Create a pool of tasks
    for prompt in concepts:
        task = asyncio.create_task(_async_generate(prompt))
        tasks.append(task)
    
    # Return the tooltips
    return await asyncio.gather(*tasks)

def _get_prompts(text: str, threshold: int):
    # Using rake algo to extract the keywords from the entire text
    prompts = []
    ranking = Rake(language_code="pt").apply(text)
    for keyword, rating in ranking:
        if rating >= MIN_KW_RATING:
            prompts.append(keyword)

    # If the text has more keywords than the threshold, we cut it down
    prompts = prompts if len(prompts) <= threshold else prompts[:threshold]
    return prompts


# Create a tooltip by hiting the replicate llama2 api
def _generate_tooltip(concept: str):
    if API_FAILSAFE:
        return """Biologia molecular é o estudo das estruturas e funções de moléculas biológicas, como proteínas, ácidos nucléicos (DNA e RNA) e lipídeos. Essas moléculas desempenham papéis fundamentais na estructura e função celular, e sua compreensão é essencial para entender os processos biológicos que ocorrem nas células vivas.
A biologia molecular envolve técnicas laboratoriais e bioinformáticas para estudar essas moléculas, como gel electrophoresis, chromatografia liquida,western blot, PCR (polymerase chain reaction), sequenciação de DNA e análise de dados bioinformatikus.
"""
    # Runs the replicate api for llama2
    # MUST HAVE THE API KEY AS AN OS ENV VARIABLE
    output = replicate.run(
        "meta/llama-2-13b-chat:f4e2de70d66816a838a89eeeb621910adffb0dd0baba3976c96980970978018d",
        input={
            "debug": False,
            "top_k": 50,
            "top_p": 1,
            "prompt": f"Me explique {concept}",
            "temperature": 0.75,
            "system_prompt": "Você é o curador de uma wiki, e precisa criar resumos para ser a introdução de um tópico. Seja o mais sucinto possível, se possível responda com no máximo dois parágrafos e retorne apenas o resumo.",
            "max_new_tokens": 500,
            "min_new_tokens": -1
        }
    )

    # It returns a generator, so we make a list out of it and append to string
    tooltip = "".join(list(output))
    return tooltip