# get candidates with the same surface form as the mention, output in WikiDisamb format

# 0       Q3918   university      The University of Nanking (金陵大学) was a private university in Nanjing, China         1
# 1       Q7894492        university      The University of Nanking (金陵大学) was a private university in Nanjing, China         0


import argparse
import json, gzip

# go to wikidata and find items with a different id but the same name for wiki2017 mapping (linked) and nils (minus)
def get_id_wrong(mapping_name):
    name_to_id = {}
    with open(mapping_name) as f:
        for l in f:
            parts = l.split("\t")
            name_to_id[parts[1].lower().replace("\n", "")] = parts[0]

    with gzip.open("../../data/wikidata-20170213-all.json.gz", 'rb', 'rb') as gf, \
            open("wrong_ids_all_mentions_with_jaccard.tsv", "w") as o:
        for ln in gf:
            if ln == b'[\n' or ln == b']\n':
                continue
            if ln.endswith(b',\n'):
                obj = json.loads(ln[:-2])
            else:
                obj = json.loads(ln)
            id = obj["id"]
            if "en" not in obj["labels"].keys():
                continue
            name = obj["labels"]["en"]["value"].lower()
            enwiki = None
            if "sitelinks" in obj and "enwiki" in obj["sitelinks"]:
                enwiki = obj["sitelinks"]["enwiki"]["title"]
            if enwiki is None:
                continue

            claims = obj["claims"]
            # print(str(claims))
            if "P279" in claims.keys():  # subclass
                # print("P279: " + str(claims["P279"]))
                continue

            if "P31" not in claims.keys():  # instance of
                continue

            # print("name: " + name)
            # print("names from map :" + str(next(iter((name_to_id.keys())))))
            # print("values from map :" + str(next(iter((name_to_id.values())))))

            if name in name_to_id.keys() and id != name_to_id[name]:
                # mention, correct 2021 id, candidate name, candidate id
                o.write(name + "\t" + name_to_id[name] + "\t" + name + "\t" + id + "\n")
            else:
                best_match = ""
                jaccard_sim_ = 0
                name_tokens = set(name.split())
                for str in name_to_id.keys() and id != name_to_id[str]:
                    mention_tokens = set(str.split())
                    jaccard_sim = len(name_tokens.intersection(mention_tokens)) / len(mention_tokens.union(name_tokens))
                    if jaccard_sim > jaccard_sim_:
                        jaccard_sim_ = jaccard_sim
                        best_match = str
                if len(best_match) > 0:
                    o.write(best_match + "\t" + name_to_id[best_match] + "\t" + name + "\t" + id + "\n")

            # todo: add triplet?


def find_candidates(input_file: str, output_file: str):
    i = 0
    with open(input_file) as f, open(output_file, "w") as fo:
        for l in f:
            line = json.loads(l)
            wikidata_id = line["wikidata_id"]
            is_nil = line["nil"]
            mention = line["mention"]

            # two wrong ones
            if is_nil:
                pass
            # once correct, one wrong
            else:
                pass

            # fo.write(str(i) + "\t" + )
            i += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input', default="test.json")

    args = parser.parse_args()
    # find_candidates(args.input)

    get_id_wrong("mapping_from_all_mentions.txt")


