#! /usr/bin/env python
import os
import sys
import json
import difflib

#{ 'document': ['terms', 'terms'],
#  'document2': ['1','2','3'],
#}
def simple_search_engine(index, query):
    return [doc_name for doc_name, terms in index.iteritems() if query in terms]

def weighted_search_engine(index, query):
    results = {}
    search_terms = query.split()
    for doc_name, terms in index.iteritems():
        matches = 0
        for search_term in search_terms:
            if search_term in terms:
                matches += 1

        rating = float(matches) / len(search_terms)
        results[doc_name] = rating

    return results

def guessy_weighted_search_engine(index, query):
    results = {}
    search_terms = query.split()
    for doc_name, terms in index.iteritems():
        matches = 0
        for search_term in search_terms:
            search_termys = difflib.get_close_matches(search_term, terms)
            for search_termy in search_termys:
                if search_termy in terms:
                    matches += 1

        rating = float(matches) / len(search_terms)
        results[doc_name] = rating

    return results


def display_search_results(engine_name, results):
    print(engine_name)
    if not results:
        print('   <No reults>')
        return
    for i, result in enumerate(results, 1):
        print('%d. %s' % (i, result))

def sort_by_score(result_dict):
    return [result
            for result, score in
            sorted(result_dict.items(), key=lambda res_score: res_score[1])
            if score > 0
        ]

def load_index(filename):
    if os.path.exists(filename):
        return json.load(open(filename))
    else:
        print("Please run:\n\tpython get_documents.py > index.txt")
        sys.exit()

if __name__ == '__main__':
    index = load_index('index.txt')
    search_query = raw_input('Search terms: ')
    print('')
    display_search_results(
        'Simple search engine returns:',
        simple_search_engine(index=index, query=search_query)
    )

    # New line for readability
    print('')
    weighted_results = weighted_search_engine(index=index, query=search_query)
    display_search_results(
        'Weighted search engine returns:',
        sort_by_score(weighted_results)
    )

    print('')
    guessy_weighted_results = guessy_weighted_search_engine(index=index, query=search_query)
    display_search_results(
        'Guessy weighted search engine returns:',
        sort_by_score(guessy_weighted_results)
    )
