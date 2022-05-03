import argparse
import json
from collections import Counter


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-n', '--nils_file', default="nil_mentions.json")

    args = parser.parse_args()

    c = Counter()

    with open(args.nils_file) as f:
        for l in f:
            line = json.loads(l)

            wikidata_id = line["wikidata_id"]

            c[wikidata_id] += 1

    print("Number of nil entities: " + str(len(c.keys())))

    print(c)
