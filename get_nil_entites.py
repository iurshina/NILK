# Compares two mappings: old and new, find the ones that are in the new but not old
import argparse
import json


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-o', '--old_wikidata_mapping')
    parser.add_argument('-n', '--new_wikidata_mapping')
    parser.add_argument('-w', '--output_file')

    args = parser.parse_args()

    old_ids = set()
    with open(args.old_wikidata_mapping) as f:
        for l in f:
            line = json.loads(l)
            id = line["id"]
            enwiki = line["enwiki"]

            old_ids.add(id)

    new_ids = set()
    mmap = {}
    with open(args.new_wikidata_mapping) as f:
        for l in f:
            line = json.loads(l)
            id = line["id"]
            enwiki = line["enwiki"]

            new_ids.add(id)
            mmap[id] = enwiki

    nil_ids = new_ids - old_ids

    print("Number of NILs: " + str(len(nil_ids)))

    with open(args.output_file, "w") as f:
        for id in nil_ids:
            f.write(id + '\t' + mmap[id] + "\n")
