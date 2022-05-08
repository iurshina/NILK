# Compares two mappings: old and new, find the ones that are in the new but not old
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-o', '--old_wikidata_mapping')
    parser.add_argument('-n', '--new_wikidata_mapping')
    parser.add_argument('-w', '--output_file')

    args = parser.parse_args()

    old_ids = set()
    with open(args.old_wikidata_mapping) as f:
        for l in f:
            parts = l.split("\t")

            old_ids.add(parts[0])

    new_ids = set()
    mmap = {}
    with open(args.new_wikidata_mapping) as f:
        for l in f:
            parts = l.split("\t")

            new_ids.add(parts[0])
            mmap[parts[0]] = parts[1]

    nil_ids = new_ids - old_ids

    print("Number of NILs: " + str(len(nil_ids)))

    with open(args.output_file, "w") as f:
        for id in nil_ids:
            enwiki = mmap[id]
            if enwiki.startswith("Category:") or enwiki.startswith("Wikipedia:") or enwiki.startswith("Module:") \
                or enwiki.startswith("Template:") or enwiki.startswith("Portal:"):
                continue
            f.write(id + '\t' + enwiki)
