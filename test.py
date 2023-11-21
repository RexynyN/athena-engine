# from transformers import T5Tokenizer # Tokenizer  
# from transformers import T5ForConditionalGeneration # PyTorch model  
from transformers import MBartForConditionalGeneration
from transformers import AutoTokenizer

# TOKENIZER_NAME = 'unicamp-dl/ptt5-base-portuguese-vocab'
# MODEL_NAME = 'phpaiola/ptt5-base-summ-xlsum'

TOKENIZER_NAME = "facebook/mbart-large-cc25"
MODEL_NAME = "GiordanoB/mbart-large-50-finetuned-summarization-V2"

tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_NAME)
model_pt = MBartForConditionalGeneration.from_pretrained(MODEL_NAME)

def summarize_text(text): 
    inputs = tokenizer.encode(text, max_length=512, truncation=True, return_tensors='pt')
    summary_ids = model_pt.generate(inputs, max_length=256, min_length=32, num_beams=5, no_repeat_ngram_size=3)
    summary = tokenizer.decode(summary_ids[0])
    return summary


text = """
Cerca de 35 milhões de argentinos estão convocados às urnas, em um país polarizado e assolado por uma das piores crises econômicas de sua história. De um lado está o ultraliberal Milei (A Liberdade Avança), que atrai o voto de protesto. De outro Massa (União pela Pátria), o peronista de centro-esquerda, que tenta pela segunda vez a escalada à Casa Rosada
Os indecisos são vistos como fiel da balança da eleição. No primeiro turno, em 22 de outubro, Massa, atual ministro da Economia, surpreendeu, e obteve 36,7% dos votos, contra 29,9% de Milei — mas 33,24% dos eleitores não votaram em nenhum dos dois candidatos.

Terceira colocada e eliminada da disputa, a conservadora Patricia Bullrich (Juntos pela Mudança), recebeu 23,8% dos votos e, para o segundo turno, decidiu apoiar Milei. Diante de uma participação de 77% do eleitorado, registrou-se 21% de votos em branco, de acordo com levantamento do Focus Group da Universidade de Buenos Aires.

Massa nos últimos dias tentou convencer os indecisos com mensagens de apaziguamento. Prometeu superar as divisões políticas com um "governo de unidade" e apelou para o "voto útil" para salvaguardar o país — que completará 40 anos de democracia ininterrupta no dia em que o novo governo tomar posse, em 10 de dezembro.

Já Milei, à frente de uma formação que inclui negacionistas da ditadura, apostou na tensão. Ele encerrou sua campanha com megacomício para 50 mil pessoas, lançando acusações de "fraudes eleitorais" — a exemplo do ex-presidente Jair Bolsonaro (PL) no Brasil

As pesquisas de intenção de voto indicam um disputa acirrada. A maioria mostra Milei alguns pontos percentuais à frente ou dois tecnicamente empatados.
"""

print(summarize_text(text))
