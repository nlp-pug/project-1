from gensim import models
from gensim.models import Word2Vec
import os

tokens_path = os.getcwd() + '/../data/sentences/'

STOPWORDS = []

class Vector:
    def __init__(self):
        self.model = None
        self.similar_words = []

    def generator(self, path):
        sentences = models.word2vec.PathLineSentences(path)
        self.model = Word2Vec(sentences, min_count=30)

    def load(self, path):
        # self.model = Word2Vec.load("vector")
        self.model = Word2Vec.load(path)

    def save(self):
        self.model.save("vector")

    def get_similar_words(self, words, threshold, depth):
        if depth == 0:
            return self.similar_words

        result = self.model.wv.most_similar(words)
        result_words = [word for word, _ in result]

        for word, prob in result:
            if word in STOPWORDS or (word, prob) in self.similar_words:
                continue
            self.similar_words.append((word, prob))
            # self.get_similar_words(words + result_words, threshold, depth - 1)
            self.get_similar_words(word, threshold, depth - 1)

    def save_similar_words(self):
        with open("similar_words.txt", 'w') as fw:
            for word in self.similar_words:
                fw.write(word[0] + '\n')


def get_stopwords():
    global STOPWORDS
    with open("百度停用词表.txt", 'r') as f:
        STOPWORDS.append(f.readline())


# vector = Vector()
# vector.generator(tokens_path)
# vector.save()
# print(vector.model.wv.most_similar("说"))

# get_stopwords()
#
# vector = Vector()
# vector.load(os.getcwd() + '/vector')
# # vector.get_similar_words(["说", "称", "表示", "声明"], 0, 5)
# # print(vector.similar_words)
# # print(len(vector.similar_words))
# # vector.save_similar_words()
# # print(vector.model.wv.most_similar(["说", "认为","陈述"]))
# # print(vector.model.wv.similarity("说", "吗"))
# print(vector.model.wv["说"])



