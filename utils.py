import os
import gzip
import json

DIR = "../../chengxi/data_process/entities_json_data/"


def get_entities_with_wikilink():
    for file in os.listdir(DIR):
        if file.startswith("till_"):
            with gzip.open(DIR + file, 'r') as f, open("entites_with_links.tsv", 'w') as el:
                for line in f:
                    line = line[:-2]  # remove comma from the end of the line (,\n)
                    j_content = json.loads(line)
                    if j_content["wiki_sitelink"] is not None:
                        el.write(j_content["id"] + "\t" + j_content["wiki_sitelink"] + "\n")


get_entities_with_wikilink()