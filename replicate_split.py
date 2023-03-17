import json


def read_ids(file_name: str):
    res = []
    with open(file_name) as f:
        for l in f:
            obj = json.loads(l)
            res.append(obj['id'])
    return res


train_ids, val_ids, test_ids = read_ids('train.jsonl'), read_ids('valid.jsonl'), read_ids('test.jsonl')

with open('all_mentions_3_03_2023.json') as f, open('train_1000.json', 'w') as tr_f, \
     open('valid_1000.json', 'w') as va_f, open('test_1000.json', 'w') as te_f:
    for l in f:
        obj = json.loads(l)
        id_ = obj['id']
        if id_ in train_ids:
            te_f.write(l)
        elif id_ in val_ids:
            va_f.write(l)
        elif id_ in test_ids:
            te_f.write(l)
