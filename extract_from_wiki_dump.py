# based on: https://github.com/RaRe-Technologies/gensim/blob/develop/gensim/scripts/segment_wiki.py


from gensim.corpora.wikicorpus import get_namespace, RE_P16, filter_wiki, remove_markup, IGNORED_NAMESPACES
import gensim.utils
import re
import json
from tqdm import tqdm
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
    title_path = "./{%(ns)s}title" % ns_mapping
    pageid_path = "./{%(ns)s}id" % ns_mapping

    text = elem.find(text_path).text
    title = elem.find(title_path).text
    pageid = elem.find(pageid_path).text

    if any(title.startswith(ignore + ':') for ignore in IGNORED_NAMESPACES):  # filter non-articles
        return []

    if text is None or len(text) == 0:
        return []

    filtered = filter_wiki(text, promote_remaining=False, simplify_links=False)

    mentions = []
    for m in re.finditer(RE_P16, filtered):
        start = m.regs[1][0]
        end = m.regs[1][1]
        mention_span = filtered[start:end]

        # [[a|b]] appears as "b" but links to page "a", thus: b https://en.wikipedia.org/wiki/Help:Link
        mention_span_parts = mention_span.split("|")
        if len(mention_span_parts) > 1:
            wikipedia_link = mention_span_parts[0]
            mention_span = mention_span_parts[1]
        else:
            wikipedia_link = mention_span_parts[0]
            mention_span = mention_span_parts[0]

        is_nil = False
        if wikipedia_link.lower() in nils.keys():
            left_context, right_context = extract_context(filtered, start, end)

            if len(left_context) < 10 and len(right_context) < 10:
                continue

            nil_wikidata_id = nils[wikipedia_link.lower()]

            mentions.append((mention_span, left_context + mention_span + right_context, len(left_context),
                             pageid, nil_wikidata_id, True))
            is_nil = True
        if not nil_only and wikipedia_link.lower() in mapping.keys():
            left_context, right_context = extract_context(filtered, start, end)

            if len(left_context) < 10 and len(right_context) < 10:
                continue

            wikidata_id = mapping[wikipedia_link.lower()]

            mentions.append((mention_span, left_context + mention_span + right_context, len(left_context),
                             pageid, wikidata_id, False))
            # making sure there is no intersection between NILs and linked entities
            if is_nil and wikidata_id == nil_wikidata_id:
                print("Error: an item is both in NILs and linked items: " + mention_span + ", " + wikidata_id)

    return mentions


def extract_context(filtered: str, start: int, end: int):
    # extract extra context so that after the markup removal, we still had enough
    left_context = filtered[max(0, start - 1000):start]
    right_context = filtered[end:min(end + 1000, len(filtered))]

    left_context = remove_markup(left_context)
    right_context = remove_markup(right_context)

    left_context = left_context[-500:]
    right_context = right_context[:500]

    return left_context, right_context


def extract_mentions(mapping, nils_file, wiki_dump, nil_only=False):
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

    with gensim.utils.open(wiki_dump, 'rb') as xml_fileobj:
        page_xmls = extract_page_xmls(xml_fileobj)

        # total - pages in 2017 wikipedia
        for xmll in tqdm(page_xmls, total=17_303_347):
            mentions = segment(xmll, nil_only=nil_only, mapping=wikidata_to_wikipedia, nils=nils)
            for mention in mentions:
                mention_span, context, offset, pageid, wikidata_id, is_nil = mention

                mention = {"mention": mention_span, "offset": offset, "length": len(mention_span), "context": context,
                                   "wikipedia_page_id": pageid, "wikidata_id": wikidata_id, "nil": is_nil}

                yield mention


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mapping', default="2017_mapping_instance_not_subclass.tsv")
    parser.add_argument("-n", "--nils", default="2021_minus_2017_instance_not_sublass.txt")
    parser.add_argument('-f', '--file', help='Path to MediaWiki database dump (read-only).',
                        default="enwiki-20170220-pages-articles.xml.bz2")
    parser.add_argument(
        '-o', '--output',
        help='Path to output file (stdout if not specified). If ends in .gz or .bz2, '
             'the output file will be automatically compressed (recommended!).',
        default="all_mentions.json")
    parser.add_argument('-x', "--nil_only", default=False)

    args = parser.parse_args()

    outfile = gensim.utils.open(args.output, 'wb')

    mentions_stream = extract_mentions(args.mapping, args.nils, args.file, args.nil_only)

    for idx, mention in enumerate(mentions_stream):
        mention["id"] = idx

        outfile.write((json.dumps(mention) + "\n").encode('utf-8'))

