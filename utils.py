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
                    line = line.replace(",\n", "").replace("]\n", "")  # remove comma from the end of the line (,\n)
                    try:
                        j_content = json.loads(line)
                    except Exception:
                        traceback.print_exc()
                        print("Error with this line: " + line)
                        continue
                    wikilink = j_content["wiki_sitelink"]
                    if wikilink is not None and not wikilink.startswith("Category:")\
                            and not wikilink.startswith("Wikipedia:") and not wikilink.startswith("Module:") \
                            and not wikilink.startswith("Template:") and not wikilink.startswith("Portal:"):
                        el.write(j_content["id"] + "\t" + wikilink + "\n")


# get_entities_with_wikilink()

# todo: tmp, remove
def convert_():
    with open("2021_minus_2027.txt") as f, open("2021_minus_2017_filtered.txt", "w") as of:
        for l in f:
            line = json.loads(l)
            id = line["id"]
            enwiki = line["enwiki"]

            if enwiki.startswith("Category:") or enwiki.startswith("Wikipedia:") or enwiki.startswith("Module:") \
                or enwiki.startswith("Template:") or enwiki.startswith("Portal:"):
                continue
            of.write(id + "\t" + enwiki + "\n")

convert_()