from actions import summarize, tooltip, sources
from quart import Quart, request

app = Quart(__name__)

@app.route('/')
async def index():
    return { "data": "We so back" }

@app.route('/tooltip', methods=["POST"])
async def tooltip_text():
    content = await request.get_json()
    if "data" not in content:
        return "O campo 'data' não foi passado, sem processamento a ser feito", 400
    
    text = content["data"]
    if not isinstance(text, str):
        return "O argumento de 'data' deve ser uma string de texto", 400
    
    words, tooltips = await tooltip.classify_from_text(content["data"])

    return { "data": { "words": words, "tooltips": tooltips } }


@app.route('/tooltip/list', methods=["POST"])
async def tooltip_concepts():
    content = await request.get_json()
    if "data" not in content:
        return "O campo 'data' não foi passado, sem processamento a ser feito", 400
    
    concepts = content["data"]
    if not isinstance(concepts, list):
        return "O argumento de 'data' deve ser uma lista de strings de texto", 400
    
    words, tooltips = await tooltip.classify_from_concept(concepts)

    return { "data": { "words": words, "tooltips": tooltips } }


@app.route("/summarize/", methods=["POST"])
async def poppers():
    content = await request.get_json()
    if "data" not in content:
        return "O campo 'data' não foi passado, sem processamento a ser feito", 400
    
    text = content["data"]
    if not isinstance(text, str):
        return "O argumento de 'data' deve ser uma string de texto", 400

    summ = summarize.summarize_text(text)

    return { "data": summ }

@app.route("/sources/", methods=["POST"])
async def further_sources():
    content = await request.get_json()
    if "data" not in content:
        return "O campo 'data' não foi passado, sem processamento a ser feito", 400
    
    concept = content["data"]
    if not isinstance(concept, str):
        return "O argumento de 'data' deve ser uma string de texto", 400

    wiki = sources.wiki_from_concept(concept)
    yt = sources.video_from_concept(concept)

    return { "data": { "video": yt, "wiki": wiki }  }

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True, use_reloader=False)
