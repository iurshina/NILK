import json


with open("all_mentions.json") as f, open("mapping_from_all_mentions.txt", "w") as fo:
    for l in f:
        line = json.loads(l)
        wikidata_id = line["wikidata_id"]
        mention = line["mention"]

        fo.write(wikidata_id + "\t" + mention + "\n")

