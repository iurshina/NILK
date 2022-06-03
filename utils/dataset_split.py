import json
from collections import Counter
import numpy as np
import random

# 80, 10, 10

# count stuff and check that we don't have both "nils" and "not nils"
c = Counter()
n_c = Counter()
with open("outputs/all_mention_01_06.json") as f, open("outputs/both_01_06.txt", "w") as out:
    for l in f:
        line = json.loads(l)
        wikidata_id = line["wikidata_id"]
        is_nil = line["nil"]

        nil_already = False
        if is_nil:
            n_c[wikidata_id] += 1
            nil_already = True
        if not is_nil:
            c[wikidata_id] += 1
            if nil_already:
                out.write(wikidata_id + "\n")

print("Finished counting")

# split keeping the ratio
buckets = {}
for id, n in n_c.items():
    k = 1
    if 1 < n < 5:
        k = 2
    if 5 <= n < 100:
        k = 3
    if 100 <= n < 1000:
        k = 4
    if 1000 <= n:
        k = 5
    if k not in buckets:
        buckets[k] = []
    buckets[k].append(id)

# split each bucket
train_ids = set()
test_ids = set()
val_ids = set()
for v in buckets.values():
    random.shuffle(v)
    train, validate, test = np.split(np.array(v), [int(.8 * len(v)), int(.9 * len(v))])
    train_ids.update(train)
    val_ids.update(validate)
    test_ids.update(test)

buckets = {}
for id, n in c.items():
    k = 1
    if 1 < n < 5:
        k = 2
    if 5 <= n < 100:
        k = 3
    if 100 <= n < 1000:
        k = 4
    if 1000 <= n:
        k = 5
    if k not in buckets:
        buckets[k] = []
    buckets[k].append(id)

for v in buckets.values():
    random.shuffle(v)
    train, validate, test = np.split(np.array(v), [int(.8 * len(v)), int(.9 * len(v))])
    train_ids.update(train)
    val_ids.update(validate)
    test_ids.update(test)

print("Starts writing")

with open("test_01_06.jsonl", "w") as test, open("train_01_06.jsonl", "w") as train, open("valid_01_06.jsonl", "w") as valid, open(
        "outputs/all_mention_01_06.json") as input:
    for l in input:
        line = json.loads(l)
        wikidata_id = line["wikidata_id"]

        if wikidata_id in train_ids:
            train.write(json.dumps(line) + "\n")
        elif wikidata_id in test_ids:
            test.write(json.dumps(line) + "\n")
        elif wikidata_id in val_ids:
            valid.write(json.dumps(line) + "\n")
        else:
            print("Id doesn't belong: " + str(wikidata_id))
