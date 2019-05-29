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
    def __init__(self, host='http://localhost', port=9123):
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
        self.full_text = None
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
        token_index = 0
        for token in self.tokens:
            # it indicate finding a word similar to "说"
            token_index += len(token)
            if token in self.words:

                logger.debug("found token {} in words, index {}".format(token,
                        self.tokens.index(token) + 1))

                speaker_index = self.get_ner(token)
                if speaker_index == None:
                    return ['no speaker', token_index]

                full_speaker = self.get_full_speaker(speaker_index)

                logger.debug("speaker is: {}".format(full_speaker))

                return [token, full_speaker]

        return ['no tokens', 0]

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
        
        # multiple nsubj
        if str(index) in self.dep_parse_dict.keys():
            dep_chunks = self.to_chunks(self.dep_parse_dict[str(index)])
            print(dep_chunks)
            if dep_chunks.count('nsubj') >= 2:
                possiable_nsubj = []
                for dep in self.dep_parse_dict[str(index)]:
                    if dep[0] == 'nsubj':
                        possiable_nsubj.append(dep)
                return min(possiable_nsubj, key=lambda x : int(x[1]) - int(x[2]))[2]
            
            

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

        
        speaker_may_start = index
        while str(speaker_may_start) in self.dep_parse_dict.keys():
            #  print(speaker_may_start)
            index_list = []
            for dep in self.dep_parse_dict[str(speaker_may_start)]:
                index_list.append(int(dep[2]))

            if min(index_list) > speaker_may_start:
                break
            else:
                speaker_may_start = min(index_list)
        #  speaker += self.tokens[index - 1]
        #  speaker += self.tokens[speaker_may_start:]

        return ''.join(self.tokens[speaker_may_start - 1:index])

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

        if str(index) not in self.dep_parse_dict.keys():
            return index

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
    
    def preprocessor(self, text):

        stop_words = ['。', '？', '！']
        #  pre_text = text.split('。')
        #  logger.debug("----------{}".format(pre_text))

        state_machine = ['None', 'FIND_ONE_Q_MARK', 'FOR_ANOTHER_Q_MARK', 'FOR_STOP_MARK', 'CUT_SENTENCE']

        state = 'FOR_STOP_MARK'
        stop_index = 0
        for index, word in enumerate(text):
            if word == '“' and state == 'FOR_STOP_MARK':
                state = 'FOR_ANOTHER_Q_MARK'
            elif word == '”' and state == 'FOR_ANOTHER_Q_MARK':
                state = 'FOR_STOP_MARK'
            elif word in stop_words and state == 'FOR_STOP_MARK':
                stop_index = index
                state = 'CUT_SENTENCE'
                break
        if state == 'CUT_SENTENCE':
            return text[0:stop_index + 1], stop_index + 1
        else:
            return text, len(text)

    def generate(self, text):

        self.full_text = text
        self.cut_text = text

        #  if len(self.preprocessor(text)) > 1:
            #  self.text = self.preprocessor(text)[0] + '。'
        #  print(self.preprocessor(text))
        while True:
            self.text, stop_index = self.preprocessor(self.cut_text)
            if stop_index == 0:
                return None

            print('------{} {}'.format(self.text, stop_index))

            self.tokens = self.nlp.word_tokenize(self.text)
            self.dependency_parse = self.nlp.dependency_parse(self.text)
            self.parse = self.nlp.parse(self.text)
            self.pos = self.nlp.pos(self.text)
            self.ner = self.nlp.ner(self.text)

            logger.debug(self.tokens)
            logger.debug(self.dependency_parse)
            logger.debug(self.parse)
            logger.debug(self.pos)
            logger.debug(self.ner)

            speaker = self.get_speaker()
            if speaker[0] == 'no tokens':
                if stop_index >= len(text):
                    return None
                else:
                    self.cut_text = self.cut_text[stop_index:]
            elif speaker[0] == 'no speaker':
                MARKS = ['，', '。', '？', '！', '；']
                for i, word in enumerate(self.cut_text[speaker[1]:]):
                    if word in MARKS:
                        self.cut_text = self.cut_text[speaker[1] + i + 1:]
                        break
            else:
                break

        if speaker[0] == 'no speaker':
            return None

        self.result['speaker'] = speaker[1]
        self.result['word_like_say'] = speaker[0]
        index = self.get_sentence_start(speaker[0])
        self.result['start_index_in_text'] = sum([len(self.tokens[i]) for i in range(index - 1)]) + stop_index
        self.result['sub_text_from_start'] = ''.join(t for t in self.tokens[index - 1:])
        if self.result['sub_text_from_start'].count('“') == 0 \
            and self.result['sub_text_from_start'].count('”') == 1:
            for i in range(index):
                if self.text[i] == '“':
                    self.result['sub_text_from_start'] = self.text[i:index] + self.result['sub_text_from_start']
                    break

        self.result['tokens'] = self.nlp.word_tokenize(self.full_text)

        sen_cut = [sen for sen in re.split("。|？|！", self.full_text) if sen != '']

        sub_sen_cut = [sen for sen in re.split("，|。|？|！", self.result['sub_text_from_start']) if sen != '']

        self.result['sen_cuts'] = sen_cut
        self.result['start_index_in_sen_cuts'] = 0
        for sen in sen_cut:
            if sub_sen_cut[0] in sen:
                self.result['start_index_in_sen_cuts'] = sen_cut.index(sen)
                self.result['start_index_in_text'] = sen.index(sub_sen_cut[0])
                #  print(sen[self.result['start_index_in_text']:])
                break

        self.clean()

        logger.debug("Parse start result: {}".format(self.result))

        return self.result

    def clean(self):
        self.full_text = None
        self.text = None
        self.tokens = None
        self.dependency_parse = None
        self.parse = None
        self.pos = None
        self.ner = None
        self.dep_parse_dict = {}

