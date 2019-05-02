'''
A sample code usage of the python package stanfordcorenlp to access a Stanford CoreNLP server.
Written as part of the blog post: https://www.khalidalnajjar.com/how-to-setup-and-use-stanford-corenlp-server-with-python/
'''

from stanfordcorenlp import StanfordCoreNLP
from nltk.tree import Tree
from nltk.tree import ParentedTree
import logging
import json

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
        with open("similar_words.txt", 'r') as f:
            content = f.read().split("\n")
            for word in content:
                if word not in self.words:
                    self.words.append(word)

    def get_speaker(self, text):
        self.text = text
        self.tokens = self.nlp.word_tokenize(text)
        self.dependency_parse = self.nlp.dependency_parse(text)
        self.parse = self.nlp.parse(text)
        self.pos = self.nlp.pos(text)

        print(self.tokens)
        print(self.dependency_parse)
        print(self.parse)
        print(self.pos)

        for token in self.tokens:
            # it indicate finding a word similar to "说"
            if token in self.words:
                print("found token {} in words".format(token))
                print(self.get_nsubj(token))
                self.read_parse_tree(token)
                return


    def get_nsubj(self, token):
        index = self.tokens.index(token) + 1

        for dep in self.dependency_parse:
            if dep[0] == 'nsubj' and dep[1] == index:
                return self.tokens[dep[2] - 1]

    def read_parse_tree(self, token):
        ptree = ParentedTree.fromstring(self.parse)
        ptree.pretty_print()
        token_location = ptree.leaf_treeposition(self.tokens.index(token))
        print(token_location)

        # print(ptree[token_location[:-5]])

        # for leave in ptree[0, 3, 2]:
        #     print(leave.label())
        sub = Tree('X', ptree[token_location[:-2]])
        print(sub.leaves())
        return sub.leaves()



if __name__ == '__main__':
    # sNLP = StanfordNLP()
    # text = 'A blog post using Stanford CoreNLP Server. Visit www.khalidalnajjar.com for more details.'
    text = '据外媒报道，英国伦敦威斯敏斯特地方法院将于5月2日开始审理向美国移交“维基揭秘”创始人朱利安?阿桑奇的问题。'
    # text = '会面结束后，郭台铭告诉媒体，他告诉特朗普，在威斯康星州的投资将会继续，预计明年5月正式投产时，能邀请特朗普亲自前往，特朗普一口答应'
    # text = '此前4月17日下午，郭台铭因“妈祖托梦”，宣布“参加2020年台湾地区领导人选举”。'
    parser = NewsParser()
    parser.get_speaker(text)
    # print("Annotate:", sNLP.annotate(text))
    # print("POS:", sNLP.pos(text))
    # print("Tokens:", sNLP.word_tokenize(text))
    # print("NER:", sNLP.ner(text))
    # print("Parse:", sNLP.parse(text))
    # print("Dep Parse:", sNLP.dependency_parse(text))

# nlp = StanfordCoreNLP('http://localhost', port=9000, lang='zh')
