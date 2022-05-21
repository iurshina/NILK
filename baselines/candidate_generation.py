# get candidates with the same surface form as the mention, output in WikiDisamb format

# 0       Q3918   university      The University of Nanking (金陵大学) was a private university in Nanjing, China         1
# 1       Q7894492        university      The University of Nanking (金陵大学) was a private university in Nanjing, China         0


import argparse


def get_id_wrong(mapping_name):
    name_to_id_mentions = {}
    with open(mapping_name) as f:
        for l in f:
            parts = l.split("\t")
            name_to_id_mentions[parts[1].lower().replace("\n", "")] = parts[0]

    name_to_id_all_wikidata = {}
    with open("name_id_wikidata_2017") as f:
        for l in f:
            parts = l.split("\t")
            name_to_id_all_wikidata[parts[1].lower().replace("\n", "")] = parts[0]

    with open("wrong_candidate_for_all_mentions.tsv") as o:
        for name in name_to_id_mentions.keys():
            mention_right_id = name_to_id_mentions[name]

            if name in name_to_id_all_wikidata.keys() and mention_right_id != name_to_id_all_wikidata[name]:
                # mention, correct 2021 id, candidate name, candidate id
                o.write(name + "\t" + mention_right_id + "\t" + name + "\t" + name_to_id_all_wikidata[name]  + "\n")
            else:
                best_match = ""
                jaccard_sim_ = 0
                mention_tokens = frozenset(name.split())
                for str in name_to_id_all_wikidata.keys():
                    if mention_right_id == name_to_id_all_wikidata[str]:
                        continue

                    candidate_tokens = frozenset(str.split())
                    jaccard_sim = len(mention_tokens.intersection(candidate_tokens)) / len(mention_tokens.union(candidate_tokens))
                    if jaccard_sim > jaccard_sim_:
                        jaccard_sim_ = jaccard_sim
                        best_match = str
                    elif jaccard_sim == jaccard_sim_:
                        # Jaccard is the same but the first token has more "value"
                        if str.split()[0] == name.split()[0]:
                            best_match = str
                    if len(best_match) > 0:
                        o.write(name + "\t" + mention_right_id + "\t" + best_match + "\t" + name_to_id_all_wikidata[best_match] + "\n")
                    else:
                        print("No candidate for " + name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input', default="test.json")

    args = parser.parse_args()
    # find_candidates(args.input)

    get_id_wrong("mapping_from_all_mentions.txt")
