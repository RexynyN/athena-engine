from pytube import Search 
import wikipedia as wp

wp.set_lang("pt")

def wiki_from_concept(concept: str) -> dict:
    query = wp.search(concept, results=1)[0]

    url = wp.page(query).url

    return { "link" : url }

def video_from_concept(concept: str) -> dict: 
    video = Search(f"explicação {concept}").results[0]

    embed_frame = f"""
    <iframe width="560" height="315" src="{video.embed_url}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen>
    </iframe>
    """
    embed_frame = embed_frame.replace("\n", "").strip()

    return { "embed": embed_frame, "name": video.title }

# print(video_from_concept("Energia Nuclear"))




