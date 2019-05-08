
import os
from collections import Counter

DATAPATH='../word2vec/data/sentences/'

class WordFreq:
    def __init__(self):
        self.counter = Counter()

    def calc_word_freq(self, path):
        for file in os.listdir(path):
            print(file)
            with open(path + file, 'r') as f:
                tokens = f.read()
                tokens = tokens.split()
                word_counter = Counter(tokens)
                self.counter.update(word_counter)

    def save(self):
        with open('counter.txt', 'w') as f:
            for k, v in self.counter.items():
                f.write('{}:{}\n'.format(k, v))

    def load(self):

        with open('counter.txt', 'r') as f:
            lines = [line.strip().split(':') for line in f]

        self.counter = Counter({line[0]: int(line[1]) for line in lines})


# wordfreq = WordFreq()
# wordfreq.calc_word_freq(DATAPATH)
# wordfreq.save()
# wordfreq.load()
