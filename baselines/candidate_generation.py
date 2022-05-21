# get candidates with the same surface form as the mention, output in WikiDisamb format

# 0       Q3918   university      The University of Nanking (金陵大学) was a private university in Nanjing, China         1
# 1       Q7894492        university      The University of Nanking (金陵大学) was a private university in Nanjing, China         0


import argparse
from tqdm import tqdm


def get_id_wrong():
    name_to_id_all_wikidata = {}
    with open("name_id_wikidata_2017.tsv") as f:
        for l in f:
            parts = l.split("\t")
            name = parts[0].lower()
            id = parts[1].replace("\n", "")
            if name not in name_to_id_all_wikidata.keys():
                name_to_id_all_wikidata[name] = []
            name_to_id_all_wikidata[name].append(id)

    with open("wrong_candidate_for_all_mentions.tsv", "w") as o, open("mapping_from_all_mentions_no_dubs.txt") as f, \
            open("no_candidates.txt", "w") as nc:
        for l in tqdm(f, total=256936):
            parts = l.split("\t")
            name = parts[1].lower().replace("\n", "")
            mention_right_id = parts[0]

            selected = ""
            if name in name_to_id_all_wikidata.keys():
                ids_candidates = name_to_id_all_wikidata[name]
                for id in ids_candidates:
                    if id != mention_right_id:
                        selected = id
                        # mention, correct 2021 id, candidate name, candidate id
                        o.write(name + "\t" + mention_right_id + "\t" + name + "\t" + selected + "\n")
                        break

            if len(selected) == 0:
                best_match = ""
                jaccard_sim_ = 0
                mention_tokens = frozenset(name.split())
                for str in name_to_id_all_wikidata.keys():
                    if len(name_to_id_all_wikidata[str]) == 1 and name_to_id_all_wikidata[str][0] == mention_right_id:
                        continue

                    candidate_tokens = frozenset(str.split())
                    jaccard_sim = len(mention_tokens.intersection(candidate_tokens)) / len(mention_tokens.union(candidate_tokens))
                    if jaccard_sim > jaccard_sim_:
                        jaccard_sim_ = jaccard_sim
                        best_match = str

                        if str.split()[0] == name.split()[0]:
                            break
                    if jaccard_sim_ > 0.8:
                        break
                if len(best_match) > 0:
                    ids_candidates = name_to_id_all_wikidata[best_match]
                    for id in ids_candidates:
                        if id != mention_right_id:
                            selected = id
                            # mention, correct 2021 id, candidate name, candidate id
                            o.write(name + "\t" + mention_right_id + "\t" + best_match + "\t" + selected + "\n")
                            break
            if len(selected) == 0:
                print("No candidate for " + name)
                nc.write(name + "\t" + mention_right_id + "\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input', default="test.json")

    args = parser.parse_args()
    # find_candidates(args.input)

    get_id_wrong()
