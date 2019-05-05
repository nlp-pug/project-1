from core_nlp import NewsParser
import os

if __name__ == '__main__':
    parser = NewsParser()
    while True:
        text = input()
        parser.get_speaker(text)