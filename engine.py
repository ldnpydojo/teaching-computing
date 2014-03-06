#! /usr/bin/env python
import json

#{ 'document': ['terms', 'terms'],
#  'document2': ['1','2','3'],
#}
def simple_search_engine(index, query):
    return [doc_name for doc_name, terms in index.iteritems() if query in terms]

if __name__ == '__main__':
    search_query = raw_input('Search terms:')
    index = json.load(open('index.txt'))
    print(
        'Simple search engine returns: %s' %
        simple_search_engine(index=index, query=search_query)
    )

    # New line for readability
    print('')
