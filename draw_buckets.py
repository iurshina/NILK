import json
from collections import Counter

import matplotlib.pylab as plt

import numpy as np
import math

# c = Counter()
# c_nil = Counter
set_c_nil = set()
set_c_not_nil = set()
m_n = 0
m_not_n = 0
with open("all_mention_01_06.json") as f:
    for l in f:
        line = json.loads(l)
        wikidata_id = line["wikidata_id"]
        is_nil = line["nil"]

        if is_nil:
            # print(str(is_nil))
            # c_nil[wikidata_id] += 1
            set_c_nil.add(wikidata_id)
            m_n += 1
        else:
            set_c_not_nil.add(wikidata_id)
            # c[wikidata_id] += 1
            m_not_n += 1


print("N entities not nil " + str(len(set_c_not_nil)))
print("N entities nil " + str(len(set_c_nil)))

print("N mentions not nil " + str(m_not_n))
print("N mentions nil " + str(m_n))

# vv = list(c.values())
# vv = sorted(vv)
#
# # vv = [1, 2, 2, 3, 3, 3, 4, 4, 5]
#
# plt.hist(vv, 5)
# plt.show()

# bins = np.linspace(math.ceil(min(vv)),
#                    math.floor(max(vv)),
#                    20) # fixed number of bins
#
# plt.xlim([min(vv)-5, max(vv)+5])
#
# plt.hist(vv, bins=bins, alpha=0.5)
# plt.title('Random Gaussian data (fixed number of bins)')
# plt.xlabel('variable X (20 evenly spaced bins)')
# plt.ylabel('count')
#
# plt.show()

# plt.hist(sorted(c.values()), 10, density=True, facecolor='g', alpha=0.75)
#
# buckets = {}
# for id, n in c.items():
#     k = "1"
#     if 1 < n < 5:
#         k = "2 to 5"
#     if 5 <= n < 100:
#         k = "6 to 100"
#     if 100 <= n < 1000:
#         k = "101 to 1000"
#     if 1000 <= n:
#         k = "1000+"
#     if k not in buckets:
#         buckets[k] = 0
#     buckets[k] += 1
#
# print(str(buckets))
# print(str(c))

#
# lists = sorted(buckets.items())
#
#
# # x = ["1", "2 to 5", "6 to 100", "101 to 1000", "1000+"]
# # y = [len(buckets["1"]), len(buckets["2 to 5"]), len(buckets["6 to 100"]), len(buckets["101 to 1000"]), len(buckets["1000+"])]
# #
# # plt.plot(x, y)
# # plt.ylabel('Number of entities')
# # plt.xlabel('Number of mentions')
# plt.show()
# # plt.savefig('buckets.png')
#
