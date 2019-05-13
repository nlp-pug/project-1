from core_nlp import NewsParser
import os

if __name__ == '__main__':
    parser = NewsParser('similar_words.txt')
    while True:
        text = input()
        parser.generate(text)
