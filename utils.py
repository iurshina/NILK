import os
import gzip
import json
import traceback


DIR = "../../chengxi/data_process/entities_json_data/"


def get_entities_with_wikilink():
    for file in os.listdir(DIR):
        if file.startswith("till_"):
            with gzip.open(DIR + file, 'rt') as f, open("entites_with_links.tsv", 'w') as el:
                print(DIR + file)
                for line in f:
                    if len(line) < 10:
                        continue
                    # print("Line: " + line)
                    line = line[:-2]  # remove comma from the end of the line (,\n)
                    try:
                        j_content = json.loads(line)
                    except Exception:
                        traceback.print_exc()
                        continue
                    if j_content["wiki_sitelink"] is not None:
                        el.write(j_content["id"] + "\t" + j_content["wiki_sitelink"] + "\n")


get_entities_with_wikilink()