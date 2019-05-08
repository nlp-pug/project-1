
import sys, os
sys.path.append(os.path.abspath('../word2vec/vector'))

from word_freq import WordFreq
from vector import Vector

class Sen2vec:
    def __init__(self):
        self.scalar_a = 1

        # load word frequency data
        self.word_freq = WordFreq()
        self.word_freq.load()
        print(self.word_freq.counter.most_common(5))

        self.word_vec = Vector()
        self.word_vec.load(os.path.abspath('../word2vec/vector/vector'))
        print(self.word_vec.model.wv["说"])

    def generate(self, sentences):
        pass


sen2vec = Sen2vec()


