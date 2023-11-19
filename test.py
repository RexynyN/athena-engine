from transformers import pipeline


summarizer = pipeline("summarization")


ARTICLE = "Energia nuclear ou energia atômica é a energia liberada em uma reação nuclear, ou seja, em processos de transformação de núcleos atômicos. Alguns isótopos de certos elementos químicos apresentam a capacidade de se transformar em outros isótopos ou elementos por meio de reações nucleares, emitindo energia durante esse processo. Baseia-se no princípio da equivalência massa-energia, proposto por Albert Einstein, segundo a qual durante reações nucleares ocorre transformação de massa em energia." 

print(summarizer(ARTICLE, max_length=130, min_length=30, do_sample=False))
