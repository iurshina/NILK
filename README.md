# NILK: Entity Linking Dataset Targeting NIL-Linking Cases

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

### Accepted to CIKM 2022, short/resource paper.

Abstract of the paper:

The NIL-linking task in Entity Linking deals with cases where the text mentions do not have a corresponding entity in the associated knowledge base. NIL-linking has two sub-tasks: NIL-detection and NIL-disambiguation. NIL-detection identifies NIL-mentions in the text. Then, NIL-disambiguation determines if some NIL-mentions refer to the same out-of-knowledge base entity. Although multiple existing datasets can be adapted for NIL-detection, none of them address the problem of NIL-disambiguation. This paper presents NILK, a new dataset for NIL-linking processing, constructed from WikiData and Wikipedia dumps from two different timestamps. The NILK dataset has two main features: 1) It marks NIL-mentions for NIL-detection by extracting mentions which belong to newly added entities in Wikipedia text. 2) It provides an entity label for NIL-disambiguation by marking NIL-mentions with WikiData IDs from the newer dump.  
