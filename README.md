# NILK

## Dataset creation steps

### Create WikiData to Wikipedia link mapping
The first step is to create mappings between WikiData ID and Wikipedia titles (links). 

```
$ python get_wikipedia_wikidata_mapping.py -w wikidata_dump -o output_file -f filter_claims

$ python get_wikipedia_wikidata_mapping.py -o 2017_mapping_instance_not_subclass.tvs -w ../../data/wikidata-20170213-all.json.gz
```

### Get NIL-entites by comparing two WikiData dumps
When you have the two mappings, you can compare them and obtain the list of out-of-knowledge-base entities.

```
$ python get_nil_entites.py -o old_wikidata_dump -n new_wikidata_dump -w output_file

$ python get_nil_entites.py -w 2021_minus_2017_instance_not_sublass.txt -o 2017_mapping_instance_not_subclass.tvs -n 2021_mapping_instance_not_subclass.tvs
```

### Get mention files from Wikipedia based on WikiData mapping
The last step is to extract context from Wikipedia pages using the two mappings. This might take a while (24-48h).
```
$ python extract_from_wiki_dump.py -m wikdata_wikipedia_mapping -n nil_mapping -o output_file -f wikipedia_dump -x nils_olny

$ python extract_from_wiki_dump.py -n 2021_minus_2017_instance_not_sublass.txt -f ../../data/enwiki-20170220-pages-articles.xml.bz2 -o nil_mentions.json -x True
```
