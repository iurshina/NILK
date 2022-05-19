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
            name_to_id[l[1].lower().replace("\n", "")] = l[0]

    with gzip.open("../../data/wikidata-20170213-all.json.gz", 'rb', 'rb') as gf, open("wrong_ids_linked_2017.tsv", "w") as o:
        for ln in gf:
            if ln == b'[\n' or ln == b']\n':
                continue
            if ln.endswith(b',\n'):
                obj = json.loads(ln[:-2])
            else:
                obj = json.loads(ln)
            id = obj["id"]
            name = obj["name"]
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

            if name.lower() in name_to_id.keys() and id != name_to_id[name]:
                o.write(name + "\t" + name_to_id[name] + "\t" + id)

            # todo: add triplet



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

    get_id_wrong("2017_mapping_instance_not_subclass.tvs")


