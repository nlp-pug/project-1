import gensim
import logging
from gensim.models.word2vec import LineSentence

paths = ['wiki_sentences.txt']
sizes = [100]

# def tran(path):
#     with open(path, "r", encoding='utf8') as f:
#         sentences = f.readline()
#
#         model = gensim.models.Word2Vec(sentences, min_count=10, size=)

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

for path in paths:
    for size in sizes:
        sentences = LineSentence(path)
        model = gensim.models.Word2Vec(sentences, min_count=10, size=size)
        modelFile = path.split('.')[0] + '_' + str(size)
        print(modelFile)
        model.save(modelFile)