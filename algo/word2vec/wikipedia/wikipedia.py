import jieba
import os
from multiprocessing import Process
import re
import time


SOURCE_PATH = os.getcwd()
database = '/../data/text/'
database_path = SOURCE_PATH + database
words_path = SOURCE_PATH + '/../data/words/'
MAX_PROCESS = 3

def get_wikipedia_dir(path):
    return [dir for dir in os.listdir(path) if dir != '.DS_Store']


def read_wikipedia_rawdata(id, dir):
    print("process {} loop for dir: {}".format(id, dir))

    for d in dir:

        for f in os.listdir(database_path + d):
            if '.DS_Store' in f:
                continue
            with open(database_path + d + '/' + f, 'r') as fs:
                print("process {} read file {}/{}".format(id, d, f))
                rawdata = fs.read()
                t1 = time.time()
                words = handle_rawdata(rawdata)
                t2 = time.time()
                print("process {} consume time {}".format(id, (t2 - t1)))
                with open(words_path + f, 'w') as fw:
                    for w in words:
                        fw.write(w + ' ')


def to_chunks(pat):
    ret = []
    for p in pat:
        if not isinstance(p, list):
            ret.append(p)
            continue
        for s in p:
            ret.append(s)
    return ret


def handle_rawdata(rawdata):
    raw = []

    # remove <doc> header and '\n'
    raw = [data for data in rawdata.split("\n") if data and re.match('(<doc)|(<\/doc>)', data) == None]

    # remove symbol like ','
    pattern = re.compile('[\w|\d]+')
    raw = [pattern.findall(r) for r in raw]

    raw = to_chunks(raw)

    # print(raw[:100])
    # jieba too slow
    words = [list(jieba.cut(r)) for r in raw]
    # print(words[:20])
    return to_chunks(words)


def cut(string):
    return list(jieba.cut(string))


def one_gram_prob(sentence):
    global words_count
    global sum_words_count
    prob = 1
    word = cut(sentence)
    for w in word:
        if words_count[w]:
            prob *= words_count[w] / sum_words_count
        else:
            prob *= 1 / sum_words_count
    return prob


def start(path):
    dir = get_wikipedia_dir(path)
    print(dir)

    process_num = MAX_PROCESS
    if len(dir) < process_num:
        process_num = len(dir)
    else:
        total_dir = []
        for i in range(MAX_PROCESS):
            dir_slice = []
            for j in range(len(dir)):
                if j % MAX_PROCESS == i:
                    dir_slice.append(dir[j])
            total_dir.append(dir_slice)

    process_list = [0] * process_num

    for i in range(process_num):
        process_list[i] = Process(target=read_wikipedia_rawdata, args=(i, total_dir[i]))
        process_list[i].start()

    for i in range(process_num):
        process_list[i].join()


start(database_path)


