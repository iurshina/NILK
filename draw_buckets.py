import json
from collections import Counter

import matplotlib.pylab as plt


c = Counter()
with open("/Users/iurshina/Desktop/test.jsonl") as f:
    for l in f:
        line = json.loads(l)
        wikidata_id = line["wikidata_id"]

        c[wikidata_id] += 1


buckets = {}
for id, n in c.items():
    k = "1"
    if 1 < n < 5:
        k = "2 to 5"
    if 5 <= n < 100:
        k = "6 to 100"
    if 100 <= n < 1000:
        k = "101 to 1000"
    if 1000 <= n:
        k = "1000+"
    if k not in buckets:
        buckets[k] = set()
    buckets[k].add(id)


lists = sorted(buckets.items())

x = ["1", "2 to 5", "6 to 100", "101 to 1000", "1000+"]
y = [len(buckets["1"]), len(buckets["2 to 5"]), len(buckets["6 to 100"]), len(buckets["101 to 1000"]), len(buckets["1000+"])]

plt.plot(x, y)
# plt.show()
plt.savefig('buckets.png')