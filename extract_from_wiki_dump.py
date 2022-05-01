# based on: https://github.com/RaRe-Technologies/gensim/blob/develop/gensim/scripts/segment_wiki.py

# JSON of mentions file
# {[{
# mention_id: 1,
# context: "Lalal",
# offset: 12,
# length: 10,
# wikipedia_page_id: ...,
# wikidata_id: Q19302, # for disambiguation
# nil: True
# }]}

# add page id and code how to extract the whole pages by page id (probably find the tool)?

# 1. Get NIL-metions file
# 1.5 Get not-NIL mentions file while checking that they are not in NIL list (use mapping for 2017)
# 2. Get All mentions file (nil and not nil for 2017 versions), delete the one from step 1

# TIME: Thu evening started, Sat morning over 1,5 days...


from gensim.corpora.wikicorpus import get_namespace, utils, RE_P16, filter_wiki, remove_markup
import gensim.utils
import re
import json
from functools import partial
import multiprocessing
import argparse

from xml.etree import ElementTree


def extract_page_xmls(f):
    """Extract pages from a MediaWiki database dump.
    Parameters
    ----------
    f : file
        File descriptor of MediaWiki dump.
    Yields
    ------
    str
        XML strings for page tags.
    """
    elems = (elem for _, elem in ElementTree.iterparse(f, events=("end",)))

    elem = next(elems)
    namespace = get_namespace(elem.tag)
    ns_mapping = {"ns": namespace}
    page_tag = "{%(ns)s}page" % ns_mapping

    for elem in elems:
        if elem.tag == page_tag:
            yield ElementTree.tostring(elem)
            # Prune the element tree, as per
            # http://www.ibm.com/developerworks/xml/library/x-hiperfparse/
            # except that we don't need to prune backlinks from the parent
            # because we don't use LXML.
            # We do this only for <page>s, since we need to inspect the
            # ./revision/text element. The pages comprise the bulk of the
            # file, so in practice we prune away enough.
            elem.clear()


def segment(page_xml, nil_only=False, mapping=None, nils=None):
    elem = ElementTree.fromstring(page_xml)
    namespace = get_namespace(elem.tag)
    ns_mapping = {"ns": namespace}
    text_path = "./{%(ns)s}revision/{%(ns)s}text" % ns_mapping
    pageid_path = "./{%(ns)s}id" % ns_mapping

    text = elem.find(text_path).text
    pageid = elem.find(pageid_path).text

    if text is None or len(text) == 0:
        return []

    filtered = filter_wiki(text, promote_remaining=False, simplify_links=False)

    mentions = []
    for m in re.finditer(RE_P16, filtered):
        start = m.regs[1][0]
        end = m.regs[1][1]
        mention_span = filtered[start:end]

        # [[a|b]] appears as "b" but links to page "a", thus: b https://en.wikipedia.org/wiki/Help:Link
        # todo: more complicated cases?
        mention_span_parts = mention_span.split("|")
        if len(mention_span_parts) > 1:
            wikipedia_link = mention_span_parts[0]
            mention_span = mention_span_parts[1]
        else:
            wikipedia_link = mention_span_parts[0]
            mention_span = mention_span_parts[0]

        is_nil = False
        if wikipedia_link in nils.keys():
            # take 500 character on each side... #todo: ???
            left_context = filtered[max(0, start - 500):start]
            right_context = filtered[end:min(end + 500, len(filtered))]
            left_context = remove_markup(left_context)
            right_context = remove_markup(right_context)

            if len(left_context) < 10 and len(right_context) < 10:
                continue

            mentions.append((mention_span, left_context + mention_span + right_context, len(left_context),
                             pageid, nils[wikipedia_link.lower()], True))
            is_nil = True
        if not nil_only and wikipedia_link in mapping.keys():
            left_context = filtered[max(0, start - 500):start]
            right_context = filtered[end:min(end + 500, len(filtered))]
            left_context = remove_markup(left_context)
            right_context = remove_markup(right_context)

            if len(left_context) < 10 and len(right_context) < 10:
                continue

            wikidata_id = mapping[wikipedia_link.lower()]

            mentions.append((mention_span, left_context + mention_span + right_context, len(left_context),
                             pageid, wikidata_id, False))
            if is_nil:
                print("Error: an item is both in NILs and linked items: " + mention_span + ", " + wikidata_id)

    return mentions


def extract_mentions(mapping, nils_file, wiki_dump, workers, nil_only=False):
    nils = {}
    with open(nils_file) as f:
        for l in f:
            parts = l.split("\t")
            nils[parts[1].lower().replace("\n", "")] = parts[0]

    wikidata_to_wikipedia = {}
    if not nil_only:
        with open(mapping) as f:
            for l in f:
                parts = l.split("\t")
                wikidata_to_wikipedia[parts[1].lower().replace("\n", "")] = parts[0]

    processes = workers
    with gensim.utils.open(wiki_dump, 'rb') as xml_fileobj:
        page_xmls = extract_page_xmls(xml_fileobj)
        pool = multiprocessing.Pool(processes)

        for group in utils.chunkize(page_xmls, chunksize=10 * processes, maxsize=1):
            for mentions in pool.imap(partial(segment, nil_only=nil_only, mapping=wikidata_to_wikipedia, nils=nils), group):
                for mention in mentions:
                    mention_span, context, offset, pageid, wikidata_id, is_nil = mention

                    mention = {"mention": mention_span, "offset": offset, "length": len(mention_span), "context": context,
                               "wikipedia_page_id": pageid, "wikidata_id": wikidata_id, "nil": is_nil}

                    yield mention

        pool.terminate()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    default_workers = max(1, multiprocessing.cpu_count() - 1)
    parser.add_argument('-m', '--mapping', default="wiki_wikidata_mapping.json")
    parser.add_argument("-n", "--nils", default="all_mentions.json")
    parser.add_argument('-f', '--file', help='Path to MediaWiki database dump (read-only).',
                        default="enwiki-20170220-pages-articles.xml.bz2")
    parser.add_argument(
        '-o', '--output',
        help='Path to output file (stdout if not specified). If ends in .gz or .bz2, '
             'the output file will be automatically compressed (recommended!).',
        default="nil_mentions.json")
    parser.add_argument('-x', "--nil_only", default=False)

    args = parser.parse_args()

    outfile = gensim.utils.open(args.output, 'wb')

    mentions_stream = extract_mentions(args.mapping, args.nils, args.file, default_workers, args.nil_only)

    for idx, mention in enumerate(mentions_stream):
        mention["id"] = idx

        outfile.write((json.dumps(mention) + "\n").encode('utf-8'))

