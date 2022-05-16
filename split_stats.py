import argparse
import json


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-f', '--file', default="train.json")

    args = parser.parse_args()

    entites = set()
    nil_m = 0
    not_nil = 0
    with open(args.file) as f:
        for l in f:
            line = json.loads(l)

            wikidata_id = line["wikidata_id"]

            entites.add(wikidata_id)

            if line["nil"]:
                nil_m += 1
            else:
                not_nil += 1

    print("Number of entities: " + str(len(entites)))
    print("Nil mentions: " + str(nil_m))
    print("Linked mentions: " + str(not_nil))


