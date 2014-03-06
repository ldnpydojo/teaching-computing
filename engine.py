#! /usr/bin/env python
import json

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

if __name__ == '__main__':
    search_query = raw_input('Search terms:')
    index = json.load(open('index.txt'))
    print(
        'Simple search engine returns: %s' %
        simple_search_engine(index=index, query=search_query)
    )

    # New line for readability
    print('')

    print(
        'Weighted search engine returns: %s' %
        weighted_search_engine(index=index, query=search_query)
    )
