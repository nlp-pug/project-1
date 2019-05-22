
import data_io
import params as para
import SIF_embedding
from scipy.spatial.distance import cosine
import jieba, re

import sys, os
sys.path.append(os.path.abspath('/home/project-01/PUG/project-1/algo/parse_sentence_start'))
from core_nlp import NewsParser



def cut(string):
    return ' '.join(jieba.cut(string))


def token(string):
    return re.findall(r'[\d|\w]+', string)


def distance(v1, v2):
    return 1 - cosine(v1, v2)


def parse_sentence_end(text):

    # input
    # word vector file, can be downloaded from GloVe website
    wordfile = '/home/project-01/PUG/data/wiki_sentences100.txt'
    # each line is a word and its frequency
    weightfile = '/home/project-01/PUG/data/word_cnt.txt'
    # the parameter in the SIF weighting scheme, usually in the range [3e-5,
    # 3e-3]
    weightpara = 1e-3
    rmpc = 1  # number of principal components to remove in SIF weighting scheme

    # load word vectors
    (words, We) = data_io.getWordmap(wordfile)
    # load word weights
    # word2weight['str'] is the weight for the word 'str'
    word2weight = data_io.getWordWeight(weightfile, weightpara)
    # weight4ind[i] is the weight for the i-th word
    weight4ind = data_io.getWeight(words, word2weight)

    # set parameters
    params = para.params()
    params.rmpc = rmpc

    parser = NewsParser('/home/project-01/PUG/data/similar_words.txt')

    result = []

    while text:
        res = parser.generate(text)
        author, start_index_in_text, sen_cuts, start_index = res['speaker'], res['start_index_in_text'], res['sen_cuts'], res['start_index_in_sen_cuts']

        sentences = [token(sen) for sen in sen_cuts]
        sentences = [' '.join(s) for s in sentences]
        sentences = [cut(s) for s in sentences]


        # load sentences
        # x is the array of word indices, m is the binary mask indicating whether
        # there is a word in that location
        x, m = data_io.sentences2idx(sentences, words)
        w = data_io.seq2weight(x, m, weight4ind)  # get word weights

        # get SIF embedding
        # embedding[i,:] is the embedding for sentence i
        embedding = SIF_embedding.SIF_embedding(We, x, w, params)


        length = len(embedding)
        end_index = start_index
        sim = -2
        while end_index + 1 < length and (sim == -2 or sim > 0.8):
            end_index += 1
            sim = distance(embedding[0], embedding[end_index])

        if sim > 0.8:
            end_index += 1

        begin = text.find(sen_cuts[start_index][start_index_in_text:])
        end = text.find(sen_cuts[end_index - 1]) + len(sen_cuts[end_index - 1]) + 1
        content = text[begin:end]

        print('Author: {}, Content: {}'.format(author, content))
        result.append({'author': author, 'content': content})

        text = text[end:]
        print('remain_text: ', text)


    return result


if __name__ == '__main__':
    parse_sentence_end("特雷莎·梅在《星期日邮报》上发表的一篇文章中声明，让我们听听选民在地方选举中所表达的呼声吧，暂时搁置我们的分歧，达成我们的协议。 据媒体报道，在周四（2日）的英国地方议会选举中，保守党失去了一千多个席位，而计划夺取数百席位的工党亦失去81席。")
