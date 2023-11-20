# from transformers import pipeline


# summarizer = pipeline("summarization")


# ARTICLE = "Energia nuclear ou energia atômica é a energia liberada em uma reação nuclear, ou seja, em processos de transformação de núcleos atômicos. Alguns isótopos de certos elementos químicos apresentam a capacidade de se transformar em outros isótopos ou elementos por meio de reações nucleares, emitindo energia durante esse processo. Baseia-se no princípio da equivalência massa-energia, proposto por Albert Einstein, segundo a qual durante reações nucleares ocorre transformação de massa em energia." 

# print(summarizer(ARTICLE, max_length=130, min_length=30, do_sample=False))





text = "Energia nuclear ou energia atômica é a energia liberada em uma reação nuclear, ou seja, em processos de transformação de núcleos atômicos. Alguns isótopos de certos elementos químicos apresentam a capacidade de se transformar em outros isótopos ou elementos por meio de reações nucleares, emitindo energia durante esse processo. Baseia-se no princípio da equivalência massa-energia, proposto por Albert Einstein, segundo a qual durante reações nucleares ocorre transformação de massa em energia.\n Foi descoberta por Otto Hahn e Lise Meitner com a observação de uma fissão nuclear depois da irradiação de urânio com nêutrons, que tinha como objetivo produzir um núcleo mais pesado. No entanto, eles descobriram que o elemento formado tinha cerca de metade da massa do urânio. Esse fato intrigou os pesquisadores, pois foi observado que um núcleo se dividiu em dois."

whitelist = [ 
        "NN",
        "NNS",
        "NNP",
        "NNPS",
        "JJ",
        "JJR",
        "JJS",
    ]



# from rake_nltk import Rake
# import nltk


text = """
O KNN (K-nearest neighbors, ou “K-vizinhos mais próximos”) costuma ser um dos primeiros algoritmos aprendidos por iniciantes no mundo do aprendizado de máquina. O KNN é muito utilizado em problemas de classificação, e felizmente é um dos algoritmos de machine learning mais fáceis de se compreender. Em resumo, o KNN tenta classificar cada amostra de um conjunto de dados avaliando sua distância em relação aos vizinhos mais próximos. Se os vizinhos mais próximos forem majoritariamente de uma classe, a amostra em questão será classificada nesta categoria. Para entender como o KNN funciona detalhadamente, primeiro considere que temos um conjunto de dados dividido em duas classes: azul e vermelho, conforme a figura abaixo.
"""
from multi_rake import Rake

rake = Rake()
ranking = rake.apply(text)
prompts = []
for keyword, rating in ranking:
    if rating >= 4:
        prompts.append(keyword)

print(prompts if len(prompts) <= 3 else prompts[:3])