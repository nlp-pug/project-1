使用Wiki数据训练词向量

数据说明：
1、下载wiki数据，约1.5G， https://dumps.wikimedia.org/zhwiki/latest/zhwiki-latest-pages-articles.xml.bz2 。这是中文维基的全部网页文件。为了抽取其中的文本信息，需要使用提取工具。
2、使用WikiExtractor提取：
    python WikiExtractor.py -b 1500M -o extracted zhwiki-latest-pages-articles.xml.bz2
   参数说明：-b表示切分的大小，默认是500K，建议设置1500M，这样提取后只有一个文件。-o就是提取的文件夹。


功能设计说明：
1、整理数据。默认使用word2vec模型进行训练。（word2vec有多种选择，这里使用gensim的实现）
word2vec输入的数据格式是句子的形式，所以第一步需要将wiki数据整理为句子。
1.1: 运行python tranData.py
    得到wiki_sentences.txt，保存了wiki数据提取的所有句子
    
2、使用word2vec模型训练，并保存训练的模型和词向量。目前提供了两种不同的包的方式，根据需要二选一即可。
2.1、使用gensim包训练
运行python tranEmb_Gensim2.0.py，训练的模型保存到wiki_sentences.100
2.2、使用word2vec包训练
运行python tranEmb_W2c.py，训练得到的模型和向量分别保存为bin和txt文件。

tips：可能需要在py文件中修改路径，或者设置词向量的维度。
tranEmb_Gensim.py已经废弃，请使用2.0
如果内存不够，请在相应文件中调整大小。
