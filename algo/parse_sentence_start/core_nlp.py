from stanfordcorenlp import StanfordCoreNLP
from collections import defaultdict
import logging
import json
import math
import os
import re


logging.basicConfig(level=logging.DEBUG, format='ParseStart:%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


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
    def __init__(self, path):
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

        with open(path, 'r') as f:
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

                logger.debug("found token {} in words, index {}".format(token,
                        self.tokens.index(token) + 1))

                speaker_index = self.get_ner(token)

                full_speaker = self.get_full_speaker(speaker_index)

                logger.debug("speaker is: {}".format(full_speaker))

                return [token, full_speaker]

        return None

    # find an speaker index in text
    def get_ner(self, token):
        FILTER_NER = ['ORGANIZATION', 'COUNTRY', 'PERSON']

        # put dependency_parse in a dict
        for dep in self.dependency_parse:
            if str(dep[1]) in self.dep_parse_dict.keys():
                self.dep_parse_dict[str(dep[1])].append(dep)
            else:
                self.dep_parse_dict[str(dep[1])] = [dep]

        logger.debug('dep_parse_dict: {0}'.format(self.dep_parse_dict))

        # corenlp is 1-index, list is 0-index, transfer
        index = self.tokens.index(token) + 1

        # start  a bfs search,
        # law1: nsubj
        #   nsubj is nominal subject,
        #   eg: he eats apple. \
        #   dep: nsubj(eats, he)
        # law2: sometimes there is not nsubj
        #   eg: 据媒体报道, 这里报道是一个状语短句，没有主语
        #   所以查找与tokens相关的person, country, org
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
        return None

    # get other words which is relative with speaker
    # eg: 英国伦敦的媒体
    #     get_ner will only get 媒体
    def get_full_speaker(self, index):
        speaker = ''

        # speaker, one word
        if str(index) not in self.dep_parse_dict.keys():
            return self.tokens[index - 1]

        for dep in self.dep_parse_dict[str(index)]:
            speaker += self.get_full_speaker(dep[2])

        speaker += self.tokens[index - 1]
        return speaker

    def get_sentence_start(self, token):

        # search dependency
        FILTER_DEP = ['dep', 'ccomp', 'pcomp', 'xcomp', 'obj', 'dobj', 'iobj', 'pobj']
        index = self.search(token, FILTER_DEP)
        # if index != self.tokens.index(token):
        logger.debug("find dependency start:{}, sentences:{}".format(index, self.tokens[index - 1:]))

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
    #    search ccomp(状语从句), get its index, find punct
    #
    # 2. others is a complement of token
    #    not ccomp, 别人修饰tokens, get tokens punct
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
                    index = min(index, dep[2])
                    logger.debug("find dep at {}".format(index))
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

    def generate(self, text):
        self.text = text
        self.tokens = self.nlp.word_tokenize(text)
        self.dependency_parse = self.nlp.dependency_parse(text)
        self.parse = self.nlp.parse(text)
        self.pos = self.nlp.pos(text)
        self.ner = self.nlp.ner(text)

        logger.debug(self.tokens)
        logger.debug(self.dependency_parse)
        logger.debug(self.parse)
        logger.debug(self.pos)
        logger.debug(self.ner)

        speaker = self.get_speaker()
        if speaker is None:
            return None

        self.result['speaker'] = speaker[1]
        self.result['word_like_say'] = speaker[0]
        index = self.get_sentence_start(speaker[0])
        self.result['start_index_in_text'] = sum([len(self.tokens[i]) for i in range(index - 1)])
        self.result['sub_text_from_start'] = ''.join(t for t in self.tokens[index - 1:])
        self.result['tokens'] = self.tokens

        sen_cut = [sen for sen in re.split("。|？|！", self.text) if sen != '']

        sub_sen_cut = [sen for sen in re.split("，|。|？|！", self.result['sub_text_from_start']) if sen != '']

        self.result['sen_cuts'] = sen_cut
        self.result['start_index_in_sen_cuts'] = None
        for sen in sen_cut:
            if sub_sen_cut[0] in sen:
                self.result['start_index_in_sen_cuts'] = sen_cut.index(sen)
                break

        self.clean()

        logger.debug("Parse start result: {}".format(self.result))

        return self.result

    def clean(self):
        self.text = None
        self.tokens = None
        self.dependency_parse = None
        self.parse = None
        self.pos = None
        self.ner = None
        self.dep_parse_dict = {}

