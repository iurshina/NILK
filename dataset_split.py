import json
from collections import Counter
import numpy as np

# 80, 10, 10

# count stuff and check that we don't have both "nils" and "not nils"
c = Counter()
n_c = Counter()
with open("all_mentions.json") as f, open("both.txt", "w") as out:
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

# split keeping the ratio
buckets = {}
for id, n in n_c.items():
    if n not in buckets:
        buckets[n] = []
    buckets[n].append(id)

print(buckets)

# split each bucket
train_ids = set()
test_ids = set()
val_ids = set()
for v in buckets.values():
    # print("Nils: " + str(len(v)))
    train, validate, test = np.split(np.array(v), [int(.8 * len(v)), int(.9 * len(v))])
    train_ids.update(train)
    val_ids.update(validate)
    test_ids.update(test)

buckets = {}
for id, n in c.items():
    if n not in buckets:
        buckets[n] = []
    buckets[n].append(id)

for v in buckets.values():
    # print("Linked: " + str(len(v)))
    train, validate, test = np.split(np.array(v), [int(.8 * len(v)), int(.9 * len(v))])
    train_ids.update(train)
    val_ids.update(validate)
    test_ids.update(test)

with open("test.json", "w") as test, open("train.json", "w") as train, open("valid.json", "w") as valid, open("all_mentions.json") as input:
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
