from rake_nltk import Rake
import nltk
import replicate
import asyncio

API_FAILSAFE = True
# nltk.download('stopwords')

def _generate_tooltip(concept):
    if API_FAILSAFE:
        return """
Biologia molecular é o estudo das estruturas e funções de moléculas biológicas, como proteínas, ácidos nucléicos (DNA e RNA) e lipídeos. Essas moléculas desempenham papéis fundamentais na estructura e função celular, e sua compreensão é essencial para entender os processos biológicos que ocorrem nas células vivas.

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

async def _async_generate(concept: str) -> str:
    return { 
        "concept": concept,
        "tooltip":  _generate_tooltip(concept) 
        } 

async def _async_generate_all(concepts: list[str]) -> list[str]:
    tasks = []
    # Create a pool of tasks
    for prompt in concepts:
        task = asyncio.create_task(_async_generate(prompt))
        tasks.append(task)
    
    # Return the tooltips
    return await asyncio.gather(*tasks)


# User passes a concept, and we return a text explaining it
async def classify_from_concept(concepts: list[str]):
    return await _async_generate_all(concepts)

# User passes a text, and we return a text explaining the core concepts of it
async def classify_from_text(text):
    whitelist = [ 
        "NN",
        "NNS",
        "NNP",
        "NNPS",
        "JJ",
        "JJR",
        "JJS",
    ]

    r = Rake()
    r.extract_keywords_from_text(text)
    prompts = []
    for rating, keyword in r.get_ranked_phrases_with_scores():
        if rating > 5:
            tokens = nltk.word_tokenize(keyword)
            possed = nltk.pos_tag(tokens)
            clean_prompt = [x for x in possed if x[1] in whitelist]
            print(clean_prompt)
            prompts.append(clean_prompt)

    return prompts if len(prompts) <= 3 else prompts[:2]