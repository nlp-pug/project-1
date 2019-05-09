'''
A sample code usage of the python package stanfordcorenlp to access a Stanford CoreNLP server.
Written as part of the blog post: https://www.khalidalnajjar.com/how-to-setup-and-use-stanford-corenlp-server-with-python/
'''

from stanfordcorenlp import StanfordCoreNLP
from nltk.tree import Tree
from nltk.tree import ParentedTree
from collections import defaultdict
import logging
import json
import math
import os

class StanfordNLP:
    def __init__(self, host='http://localhost', port=9000):
        self.nlp = StanfordCoreNLP(host, port=port,
                                   timeout=30000, lang='zh')  # , quiet=False, logging_level=logging.DEBUG)
        self.props = {
            'annotators': 'tokenize,ssplit,pos,ner,parse,depparse',
            'pipelineLanguage': 'zh',
            # 'outputFormat': 'text'
            'outputFormat': 'json'
        }

    def word_tokenize(self, sentence):
        return self.nlp.word_tokenize(sentence)

    def pos(self, sentence):
        return self.nlp.pos_tag(sentence)

    def ner(self, sentence):
        return self.nlp.ner(sentence)

    def parse(self, sentence):
        return self.nlp.parse(sentence)

    def dependency_parse(self, sentence):
        return self.nlp.dependency_parse(sentence)

    def annotate(self, sentence):
        return json.loads(self.nlp.annotate(sentence, properties=self.props))
        # return self.nlp.annotate(sentence, properties=self.props)

    @staticmethod
    def tokens_to_dict(_tokens):
        tokens = defaultdict(dict)
        for token in _tokens:
            tokens[int(token['index'])] = {
                'word': token['word'],
                'lemma': token['lemma'],
                'pos': token['pos'],
                'ner': token['ner']
            }
        return tokens


class NewsParser:
    def __init__(self):
        self.nlp = StanfordNLP()
        self.words = []
        self.text = None
        self.tokens = None
        self.dependency_parse = None
        self.parse = None
        self.pos = None
        self.ner = None
        self.dep_parse_dict = {}
        self.result = {}

        with open("similar_words.txt", 'r') as f:
            content = f.read().split("\n")
            for word in content:
                if word not in self.words:
                    self.words.append(word)

    def cut(self, text):
        return self.nlp.word_tokenize(text)


    def get_speaker(self):
        for token in self.tokens:
            # it indicate finding a word similar to "说"
            if token in self.words:
                print("found token {} in words, index {}".format(token,
                        self.tokens.index(token) + 1))
                speaker_index = self.get_ner(token)
                print("------------ {}".format(self.get_full_speaker(speaker_index)))
                return [token, self.get_full_speaker(speaker_index)]

    # get nominal subject
    def get_ner(self, token):
        FILTER_NER = ['ORGANIZATION', 'COUNTRY', 'PERSON']
        # create dependency parse dict for search
        for dep in self.dependency_parse:
            if str(dep[1]) in self.dep_parse_dict.keys():
                self.dep_parse_dict[str(dep[1])].append(dep)
            else:
                self.dep_parse_dict[str(dep[1])] = [dep]

        print(self.dep_parse_dict)

        index = self.tokens.index(token) + 1

        path = [str(index)]

        seen = []

        while len(path):
            node = path.pop(0)

            if node in seen or node not in self.dep_parse_dict:
                continue

            for dep in self.dep_parse_dict[node]:
                if dep[0] == 'nsubj' or self.ner[dep[2] - 1][1] in FILTER_NER:
                    return dep[2]
                else:
                    path.append(str(dep[2]))

            seen.append(node)

        # not found
        return -1

    def get_full_speaker(self, index):
        speaker = ''

        # speaker, one word
        if str(index) not in self.dep_parse_dict.keys():
            return self.tokens[index - 1]

        for dep in self.dep_parse_dict[str(index)]:
            speaker += self.get_full_speaker(dep[2])
            # speaker += self.tokens[dep[2] - 1]

        speaker += self.tokens[index - 1]
        return speaker

    # I try to get token's sub-tree
    def get_sentence_start(self, token):
        # ptree = Tree.fromstring(self.parse)
        # ptree.pretty_print()
        # # ptree.draw()
        #
        # print(self.tokens[self.tokens.index(token):])
        # return self.tokens[self.tokens.index(token):]

        # ptree = ParentedTree.fromstring(self.parse)
        # # ptree.pretty_print()
        # ptree.draw()
        # token_location = ptree.leaf_treeposition(self.tokens.index(token))
        # print(token_location)
        #
        # sub = Tree('X', ptree[token_location[:-2]])
        # print(sub.leaves())
        # print(sub.label())
        # return sub.leaves()

        # search dependency
        FILTER_DEP = ['dep', 'ccomp', 'pcomp', 'xcomp', 'obj', 'dobj', 'iobj', 'pobj']
        index = self.search(token, FILTER_DEP)
        # if index != self.tokens.index(token):
        print("find dependency start:{}, word:{}".format(index, self.tokens[index - 1:]))

        return index


    # find a minimum index in dependency tree
    # eg: [phrase1]-dep-[phrase2]-ccomp-[phrase3]-[phrase4]
    # 1. find a word similar with "say" in phrase3,
    # 2. search dependency with other phrase
    # 3. ok, find phrase2, but phrase dependency with phrase1
    # 4. and index(phrase1) < index(phrase2)
    # 5. go on search, find phrase1
    # 6. no more index smaller than phrase1
    # 7. stop and return phrase
    # two strategy:
    # 1. token is a complement of others
    # 2. others is a complement of token
    def search(self, token, filter):
        token_index = index = self.tokens.index(token) + 1

        path = [str(index)]

        seen = []

        while len(path):
            node = path.pop(0)

            if node in seen or node not in self.dep_parse_dict:
                continue

            for dep in self.dep_parse_dict[node]:
                if dep[0] in filter:
                    # if index == token_index:
                    #     index = dep[2]
                    # else:
                    index = min(index, dep[2])
                    print("find dep at {}".format(index))
                    path.append(str(dep[2]))

            seen.append(node)

        punct_left = math.inf
        index_list = [index]
        if 'punct' not in self.to_chunks(self.dep_parse_dict[str(index)]):
            for key, dep in self.dep_parse_dict.items():
                if index in self.to_chunks(dep):
                    if 'punct' in self.to_chunks(dep):
                        index_list.append(int(key))

        for idx in index_list:
            for dep in self.dep_parse_dict[str(idx)]:
                if dep[0] == 'punct':
                    punct_left = min(punct_left, dep[2])

        return punct_left

    def to_chunks(self, _list):
        chunks = []
        for v in _list:
            for t in v:
                chunks.append(t)
        return chunks

    def search_all(self, token, filter):
        filter += ['nsubj']
        token_index = index = self.tokens.index(token) + 1

        for key, dep in self.dep_parse_dict:
            if dep[2] == token_index:
                pass

    def generate(self, text):
        self.text = text
        self.tokens = self.nlp.word_tokenize(text)
        self.dependency_parse = self.nlp.dependency_parse(text)
        self.parse = self.nlp.parse(text)
        self.pos = self.nlp.pos(text)
        self.ner = self.nlp.ner(text)

        print(self.tokens)
        print(self.dependency_parse)
        print(self.parse)
        print(self.pos)
        print(self.ner)

        speaker = self.get_speaker()
        self.result['speaker'] = speaker[1]
        self.result['word_like_say'] = speaker[0]
        index = self.get_sentence_start(speaker[0])
        self.result['sub_sen'] = ''.join(t for t in self.tokens[index - 1:])
        self.result['tokens'] = self.tokens

        self.clean()

        return self.result

    def clean(self):
        self.text = None
        self.tokens = None
        self.dependency_parse = None
        self.parse = None
        self.pos = None
        self.ner = None
        self.dep_parse_dict = {}
        self.result = {}



if __name__ == '__main__':
    # sNLP = StanfordNLP()
    # text = 'A blog post using Stanford CoreNLP Server. Visit www.khalidalnajjar.com for more details.'
    text = '据外媒报道，英国伦敦威斯敏斯特地方法院将于5月2日开始审理向美国移交“维基揭秘”创始人朱利安?阿桑奇的问题。'
    # text = '会面结束后，郭台铭告诉媒体，他告诉特朗普，在威斯康星州的投资将会继续，预计明年5月正式投产时，能邀请特朗普亲自前往，特朗普一口答应'
    # text = '此前4月17日下午，郭台铭因“妈祖托梦”，宣布“参加2020年台湾地区领导人选举”。'
    parser = NewsParser()
    parser.generate(text)
    # print("Annotate:", sNLP.annotate(text))
    # print("POS:", sNLP.pos(text))
    # print("Tokens:", sNLP.word_tokenize(text))
    # print("NER:", sNLP.ner(text))
    # print("Parse:", sNLP.parse(text))
    # print("Dep Parse:", sNLP.dependency_parse(text))

# nlp = StanfordCoreNLP('http://localhost', port=9000, lang='zh')
