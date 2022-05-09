# Get a mapping wikipedia link to wikidata id by processing WikiData dumb
import argparse
import gzip
import json

# {
#       "property" : {
#         "type" : "uri",
#         "value" : "http://www.wikidata.org/entity/P31"
#       },
#       "propertyLabel" : {
#         "xml:lang" : "en",
#         "type" : "literal",
#         "value" : "instance of"
#       }
# }

# {
#       "property" : {
#         "type" : "uri",
#         "value" : "http://www.wikidata.org/entity/P279"
#       },
#       "propertyLabel" : {
#         "xml:lang" : "en",
#         "type" : "literal",
#         "value" : "subclass of"
#       }
#     }
# }


def get_mapping(wikidata_path, filter_claims):
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

            if filter_claims:
                claims = obj["claims"]
                if "P279" in claims.keys():  # subclass
                    print("P279: " + str(claims["P279"]))
                    continue

                if "P31" not in claims.keys():  # instance of
                    continue

            yield id, enwiki


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-w', '--wikidata', default="")
    parser.add_argument('-f', '--filter_claims', default=False)
    parser.add_argument('-o', '--output', default="wiki_wikidata_mapping.json")

    args = parser.parse_args()

    with open(args.output, "w") as out:
        for id, enwiki in get_mapping(args.wikidata, args.filter_claims):
            out.write(id + "\t" + enwiki + "\n")