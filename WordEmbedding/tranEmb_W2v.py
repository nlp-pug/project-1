import word2vec
import fire
from tqdm import tqdm

paths = ['wiki_sentences.txt']
sizes = [100]

def tran(path):
    model = word2vec.load(path)
    vocab, vectors = model.vocab, model.vectors
    print(path)
    print('shape of word embeddings: ', vectors.shape)

    new_path = path.split('.')[0] + '.txt'
    print('transform start...')
    with open(new_path, "w") as f:
        for word, vector in tqdm(zip(vocab, vectors)):
            f.write(str(word) + ' ' + ' '.join(map(str, vector)) + '\n')
    print('Transform Complete!\n')

for path in paths:
    for size in sizes:
        with open(path, "r", encoding='utf8') as f:
            # emb_path is model's path
            emb_path = path.split('.')[0] + str(size) + '.bin'
            word2vec.word2vec(path, emb_path, min_count=5, size=size, verbose=True)
            tran(emb_path)
