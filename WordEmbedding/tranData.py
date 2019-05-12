import glob
import errno
import re
from hanziconv import HanziConv
import jieba
from tqdm import tqdm

filePath = '/home/lc/project-1/WordEmbedding/DATA/extracted/AA/wiki_**'
files = glob.glob(filePath)

# get all articles words
allArticles = []

for name in files:
    try:
        textFile = open(name, "r", encoding="utf8")
        lines = textFile.readlines()
        allArticles.append(lines)
    except IOError as exc:
        if exc.errno != errno.EISDIR:
            raise

print('len of all articles: ', len(allArticles[0]))

# remove useless lines in articles
text = []
#for articles in allArticles[0][:100]:
print(' remove useless lines in articles ')
for articles in tqdm(allArticles[0]):
    flag = True
    for element in articles:
        if element.startswith('<doc id') or element.startswith('</doc>') or element.startswith('<doc'):
            flag = False
    if flag :
        text.append(articles)

del allArticles

# remain only word and numbers
def findAllTokens(string):
    return ' '.join(re.findall('[\w|\d]+', string))

print(' remain word and numbers ')
textTokens = [findAllTokens(x) for x in tqdm(text)]
# print(text[:100])
del text

# change to simplified
print(' change to simplified ')
textTokens = [HanziConv.toSimplified(x) for x in tqdm(textTokens)]


# use jieba to cut words
print(' tokenization ')
def cut(string): return list(jieba.cut(string))
allTokens = [cut(x) for x in tqdm(textTokens)]

# print(textTokens[:100])
del textTokens

# get off space
print (' get off space ')
validTokens = [[t for t in x if t.strip() ]
               for x in tqdm(allTokens) if len(x)>0 and x[0]!='doc']

# print(allTokens[:100])
del allTokens

# print(validTokens[:100])
# join list to sentence
print( 'generate sentences ')
#sentences = [' '.join(x) for x in tqdm(validTokens)]

with open('wiki_sentences.txt', 'w') as f:
    for x in tqdm(validTokens):
        sentence = ' '.join(x)
        f.write(sentence+'\n')
        #f.writelines([sentence+'\n' for sentence in sentences])












