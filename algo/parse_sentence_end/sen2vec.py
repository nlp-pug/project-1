import sys, os
import re
import numpy as np
from numpy import linalg as la
from scipy.spatial.distance import cosine

sys.path.append(os.path.abspath('../word2vec/vector'))
sys.path.append(os.path.abspath('../parse_sentence_start'))
from word_freq import WordFreq
from vector import Vector
from core_nlp import NewsParser


class Sen2vec:
    def __init__(self):
        self.scalar_a = 0.0001

        # load word frequency data
        self.word_freq = WordFreq()
        self.word_freq.load()

        self.word_vec = Vector()
        self.word_vec.load(os.path.abspath('../word2vec/vector/vector'))

        self.parser = NewsParser()

        # self.word_sum_count =
        # for k, v in self.word_freq.counter.items():
        #     self.word_sum_count += int(v)
        # print("----{}".format(self.word_sum_count))

    def get_vec(self, sentences):
        # cut to small sentence
        sentences = [sen for sen in re.split("，|。|？|！", sentences)]

        all_sen_vec = []
        for sen in sentences:
            if len(sen) <= 0:
                continue

            tokens = self.parser.cut(sen)

            sen_vec = 0
            for token in tokens:
                freq = self.word_freq.counter[token]
                vec = self.word_vec.model.wv[token]
                print("word:{} freq: {}".format(token, freq))
                print("word vec: {}, type {}".format(vec, type(vec)))

                sen_vec += self.scalar_a / (self.scalar_a + freq / self.word_freq.sum) * vec

            sen_vec *= 1.00000 / len(tokens)
            all_sen_vec.append(sen_vec)
            # print("stage1: sentence vec: {}".format(sen_vec))

        print("----all sen---{}".format(all_sen_vec))
        matrix = np.array(all_sen_vec)
        u, sigma, vt = la.svd(matrix.T)
        # print("----u{}".format(u))
        # print("----simga{}".format(sigma))
        # print("----v{}".format(vt))

        v1 = vt[0][np.newaxis]
        print("vt is -------------{} {}".format(v1, np.dot(v1, v1.T)))

        all_sen_vec = [vec - np.dot(v1, v1.T) * vec for vec in all_sen_vec]
        print("---------------result-------------------")
        print(all_sen_vec[0])
        print("============")
        print(all_sen_vec[1])

        for vec in all_sen_vec:
            print("----------{}".format(self.get_cos(all_sen_vec[0], vec)))

    def get_cos(self, v1, v2):
        return cosine(v1, v2)





if __name__ == '__main__':
    sen2vec = Sen2vec()
    while True:
        text = input()
        sen2vec.get_vec(text)
