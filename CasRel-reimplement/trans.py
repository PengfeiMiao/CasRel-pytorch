# _*_ coding:utf-8 _*_

import json
from tqdm import tqdm
import codecs
import jieba

all_50_schemas = set()
data_path = 'data/BAIKE'
cache_path = 'cache/data/BAIKE'

# jieba.load_userdict(data_path + '/dict.txt')

with open(data_path + '/all_50_schemas', 'r', encoding='utf-8') as f:
    for l in tqdm(f):
        a = json.loads(l)
        all_50_schemas.add(a['predicate'])

id2predicate = {i: j for i, j in enumerate(all_50_schemas)}  # 0表示终止类别
predicate2id = {j: i for i, j in id2predicate.items()}

with codecs.open(cache_path + '/rel2id.json', 'w', encoding='utf-8') as f:
    json.dump([id2predicate, predicate2id], f, indent=4, ensure_ascii=False)

chars = {}
min_count = 2

train_data = []
# spo_list / triple_list
with open(data_path + '/train_data.json', 'r', encoding='utf-8') as f:
    for l in tqdm(f):
        a = json.loads(l)
        text = a['text']
        text = ' '.join(list(jieba.cut(text)))
        train_data.append(
            {
                'text': text,
                'triple_list': [
                    (
                        ' '.join(jieba.cut(i['subject'])),
                        i['predicate'],
                        ' '.join(jieba.cut(i['object']))
                    ) for i in a['spo_list']
                ]
            }
        )
        for c in a['text']:
            chars[c] = chars.get(c, 0) + 1

with codecs.open(cache_path + '/train_triples.json', 'w', encoding='utf-8') as f:
    json.dump(train_data, f, indent=4, ensure_ascii=False)

dev_data = []

with open(data_path + '/dev_data.json', 'r', encoding='utf-8') as f:
    for l in tqdm(f):
        a = json.loads(l)
        text = a['text']
        text = ' '.join(list(jieba.cut(text)))
        dev_data.append(
            {
                'text': text,
                'triple_list': [
                    (
                        ' '.join(jieba.cut(i['subject'])),
                        i['predicate'],
                        ' '.join(jieba.cut(i['object']))
                    ) for i in a['spo_list']
                ]
            }
        )
        for c in a['text']:
            chars[c] = chars.get(c, 0) + 1

with codecs.open(cache_path + '/dev_triples.json', 'w', encoding='utf-8') as f:
    json.dump(dev_data, f, indent=4, ensure_ascii=False)

# with codecs.open(data_path + '/all_chars.json', 'w', encoding='utf-8') as f:
#     chars = {i: j for i, j in chars.items() if j >= min_count}
#     id2char = {i + 2: j for i, j in enumerate(chars)}  # padding: 0, unk: 1
#     char2id = {j: i for i, j in id2char.items()}
#     json.dump([id2char, char2id], f, indent=4, ensure_ascii=False)
