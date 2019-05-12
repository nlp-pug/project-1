import gensim

model = gensim.models.Word2Vec.load('wiki_sentences_100')
# '(min_count=10, size=100)

model['中国']