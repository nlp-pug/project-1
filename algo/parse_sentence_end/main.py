
import data_io
import params
import SIF_embedding
# import collections



def parse_sentence_end(text):

    # input
    # word vector file, can be downloaded from GloVe website
    wordfile = './glove.840B.300d.txt'
    weightfile = '../auxiliary_data/enwiki_vocab_min200.txt' # each line is a word and its frequency
    # weightfile = collections.Counter()
    # the parameter in the SIF weighting scheme, usually in the range [3e-5, 3e-3]
    weightpara = 1e-3
    rmpc = 1  # number of principal components to remove in SIF weighting scheme


    # load word vectors
    (words, We) = data_io.getWordmap(wordfile)
    # load word weights
    # word2weight['str'] is the weight for the word 'str'
    word2weight = data_io.getWordWeight(weightfile, weightpara)
    # weight4ind[i] is the weight for the i-th word
    weight4ind = data_io.getWeight(words, word2weight)
    # load sentences
    # x is the array of word indices, m is the binary mask indicating whether
    # there is a word in that location
    x, m = data_io.sentences2idx(sentences, words)
    w = data_io.seq2weight(x, m, weight4ind)  # get word weights

    # set parameters
    params = params.params()
    params.rmpc = rmpc
    # get SIF embedding
    # embedding[i,:] is the embedding for sentence i
    embedding = SIF_embedding.SIF_embedding(We, x, w, params)

    print(embedding)


if __name__ == '__main__':
    parse_sentence_end("这是一个测试。哈哈！")
