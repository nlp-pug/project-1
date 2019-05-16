## How to use

1. activate environment

```shell
conda activate nlp-pug
```



2. start stanford CoreNLP

```shell
# go to /home/stu/project-01/PUG/data
# start script on background
./start_corenlp.sh &
```



3. use

```shell
# go to /home/stu/project-01/PUG/project-1/algo/parse_sentence_start
```

```
.
├── README.md
├── core_nlp.py 
├── similar_words.txt
├── start_corenlp.sh
├── test_corenlp.py
└── text_case.txt
```

the interface is in core_nlp.py

Usage:

```
parser = NewsParser('similar_words.txt')
result = parser.generate(text)
```

Here, result is a dict like

```shell
# 特雷莎·梅在《星期日邮报》上发表的一篇文章中声明，让我们听听选民在地方选举中所表达的呼声吧，暂时搁置我们的分歧，达成我们的协议。
{'speaker': '特雷莎·梅', 'word_like_say': '声明', 'start_index_in_text': 24, 'sub_text_from_start': '，让我们听听选民在地方选举中所表达的呼声吧，暂时搁置我们的分歧，达成我们的协议。', 'tokens': ['特雷莎·梅', '在', '《', '星期日', '邮报', '》', '上', '发表', '的', '一', '篇', '文章', '中', '声明', '，', '让', '我们', '听听', '选民', '在', '地方', '选举', '中', '所', '表达', '的', '呼声', '吧', '，', '暂时', '搁置', '我们', '的', '分歧', '，', '达成', '我们', '的', '协议', '。'], 'sen_cuts': ['特雷莎·梅在《星期日邮报》上发表的一篇文章中声明', '让我们听听选民在地方选举中所表达的呼 声吧', '暂时搁置我们的分歧', '达成我们的协议'], 'start_index_in_sen_cuts': 1}
```

you may need 'speaker', 'sub_sen_index'(index where sentence start in text), 'tokens'

4. more test

see test_corenlp.py and text_case.txt
