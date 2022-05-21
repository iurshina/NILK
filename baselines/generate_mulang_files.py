# 0       Q3918   university      The University of Nanking (金陵大学) was a private university in Nanjing, China         1
# 1       Q7894492        university      The University of Nanking (金陵大学) was a private university in Nanjing, China         0

import json

wrong_cand_map = {}
with open("wrong_candidate_for_all_mentions.tsv", "w") as f:
    for l in f:
        parts = l.split("\t")
        wrong_cand_map[parts[0] + parts[1]] = parts[3].replace("\n", "")

i = 0
with open("test.tsv") as inp, open("test_m.tsv", "w") as o:
    for l in inp:
        line = json.loads(l)
        id = line["id"]
        mention = line["mention"]
        nil = line["nil"]
        wiki_id = line["wikidata_id"]

        context = line["context"]
        offset = line["offset"]

        sent = context[max(offset - 50, 0):offset] + context[offset:offset + len(mention)] + context[offset + len(mention):offset + len(mention)+50]

        if nil:
            cand_id = wrong_cand_map[mention + wiki_id]
            o.write(str(i) + "\t" + cand_id + "\t" + mention + "\t" + sent + "\t" + str(0) + "\n")
        else:
            # correct one
            o.write(str(i) + "\t" + wiki_id + "\t" + mention + "\t" + sent + "\t" + str(1) + "\n")
            i += 1
            # wrong one
            cand_id = wrong_cand_map[cand_id + wiki_id]
            o.write(str(i) + "\t" + cand_id + "\t" + mention + "\t" + sent + "\t" + str(0) + "\n")
        i += 1