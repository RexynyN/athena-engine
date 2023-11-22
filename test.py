from pytube import Search 


def wiki_from_concept(concept: str) -> dict:
    pass 
def video_from_concept(concept: str) -> dict: 
    video = Search(f"explicação {concept}").results[0]

    embed_frame = f"""
    <iframe width="560" height="315" src="{video.embed_url}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen>
    </iframe>
    """
    embed_frame = embed_frame.replace("\n", "").strip()

    return { "embed": embed_frame, "name": video.title }

# print(video_from_concept("Energia Nuclear"))



import wikipedia as wp

wp.set_lang("pt")

query = wp.search("ensinamentos de platão", results = 5)
print(query)

print(wp.page(query).url)
