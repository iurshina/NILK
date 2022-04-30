# Get a mapping wikipedia link to wikidata id by processing WikiData dumb
import argparse
import gzip
import json


def get_mapping(wikidata_path):
    with gzip.open(wikidata_path, 'rb') as gf:
        for ln in gf:
            if ln == b'[\n' or ln == b']\n':
                continue
            if ln.endswith(b',\n'):
                obj = json.loads(ln[:-2])
            else:
                obj = json.loads(ln)
            id = obj["id"]
            enwiki = None
            if "sitelinks" in obj and "enwiki" in obj["sitelinks"]:
                enwiki = obj["sitelinks"]["enwiki"]["title"]
            if enwiki is None:
                continue

            yield id, enwiki


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-w', '--wikidata', default="")

    args = parser.parse_args()

    with open("wiki_wikidata_mapping.json", "w") as out:
        for id, enwiki in get_mapping(args.wikidata):
            out.write(json.dumps({"id": id, "enwiki": enwiki}) + "\n")