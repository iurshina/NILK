# Get a mapping wikipedia link to wikidata id by processing WikiData dumb
import argparse
import gzip
import json


def get_mapping(wikidata_path):
    with gzip.open(wikidata_path, 'rt') as gf:
        for ln in gf:
            if ln == b'[\n' or ln == b']\n':
                continue
            if ln.endswith(b',\n'):
                obj = json.loads(ln[:-2])
            else:
                obj = json.loads(ln)
            id = obj["id"]
            wikisite_link = obj["wiki_sitelink"]
            enwiki = ""
            if "sitelinks" in obj and "enwiki" in obj["sitelinks"]:
                enwiki = obj["sitelinks"]["enwiki"]["title"]

            yield id, wikisite_link, enwiki


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    parser.add_argument('-w', '--wikidata', default="")

    with open("wiki_wikidata_mapping.json", "w") as out:
        for id, sitelink, enwiki in get_mapping(args.wikidata):
            out.write(json.dumps({"id": id, "sitelink": sitelink, "enwiki": enwiki}))