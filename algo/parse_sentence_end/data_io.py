# -*- coding: utf-8 -*-
# @Author: qirui
# @Date:   2019-05-10 10:47:10
# @Last Modified by:   qirui
# @Last Modified time: 2019-05-23 01:17:05
# @E-mail: 2596688048@qq.com


import numpy as np


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def getWordmap(textfile):
    #  return {}, []
    words = {}
    We = []
    f = open(textfile, 'r', encoding='UTF-8')
    lines = f.readlines()

    for (n, i) in enumerate(lines):

        # print(n, i)

        i = i.split()
        j = 1
        v = []

        # if len(i) > 1 and not isfloat(i[1]):
        #     continue

        while j < len(i):
            v.append(float(i[j]))
            j += 1
        words[i[0]] = n
        We.append(v)
    return (words, np.array(We))


def getWordWeight(weightfile, a=1e-3):
    if a <= 0:  # when the parameter makes no sense, use unweighted
        a = 1.0

    word2weight = {}
    with open(weightfile) as f:
        lines = f.readlines()
    N = 0
    for i in lines:
        i = i.strip()
        if(len(i) > 0):
            i = i.split()
            if(len(i) == 2):
                word2weight[i[0]] = float(i[1])
                N += float(i[1])
            else:
                print(i)
    for key, value in word2weight.items():
        word2weight[key] = a / (a + value / N)
    return word2weight


def getWeight(words, word2weight):
    weight4ind = {}
    for word, ind in words.items():
        if word in word2weight:
            weight4ind[ind] = word2weight[word]
        else:
            weight4ind[ind] = 1.0
    return weight4ind


def prepare_data(list_of_seqs):
    lengths = [len(s) for s in list_of_seqs]
    n_samples = len(list_of_seqs)
    maxlen = np.max(lengths)
    x = np.zeros((n_samples, maxlen)).astype('int32')
    x_mask = np.zeros((n_samples, maxlen)).astype('float32')
    for idx, s in enumerate(list_of_seqs):
        x[idx, :lengths[idx]] = s
        x_mask[idx, :lengths[idx]] = 1.
    x_mask = np.asarray(x_mask, dtype='float32')
    return x, x_mask


def lookupIDX(words, w):
    w = w.lower()
    if len(w) > 1 and w[0] == '#':
        w = w.replace("#", "")
    if w in words:
        return words[w]
    elif 'UUUNKKK' in words:
        return words['UUUNKKK']
    else:
        return len(words) - 1


def getSeq(p1, words):
    p1 = p1.split()
    X1 = []
    for i in p1:
        X1.append(lookupIDX(words, i))
    return X1


def sentences2idx(sentences, words):
    """
    Given a list of sentences, output array of word indices that can be fed into the algorithms.
    :param sentences: a list of sentences
    :param words: a dictionary, words['str'] is the indices of the word 'str'
    :return: x1, m1. x1[i, :] is the word indices in sentence i, m1[i,:] is the mask for sentence i (0 means no word at the location)
    """

    seq1 = []
    for i in sentences:
        seq1.append(getSeq(i, words))
    x1, m1 = prepare_data(seq1)
    return x1, m1


def seq2weight(seq, mask, weight4ind):
    weight = np.zeros(seq.shape).astype('float32')
    for i in range(seq.shape[0]):
        for j in range(seq.shape[1]):
            if mask[i, j] > 0 and seq[i, j] >= 0:
                weight[i, j] = weight4ind[seq[i, j]]
    weight = np.asarray(weight, dtype='float32')
    return weight
