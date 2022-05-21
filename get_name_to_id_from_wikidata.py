import json, gzip


with gzip.open("../../data/wikidata-20170213-all.json.gz", 'rb', 'rb') as gf, \
        open("name_id_wikidata_2017.tsv", "w") as o:
    for ln in gf:
        if ln == b'[\n' or ln == b']\n':
            continue
        if ln.endswith(b',\n'):
            obj = json.loads(ln[:-2])
        else:
            obj = json.loads(ln)
        id = obj["id"]
        if "en" not in obj["labels"].keys():
            continue
        name = obj["labels"]["en"]["value"].lower()
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

        o.write(name + '\t' + id + '\n')