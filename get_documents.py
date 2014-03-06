from imdbpie import Imdb
import json


def get_documents(number_of_films=10):
    imdb = Imdb({'anonymize': False})
    titles_and_ids = [{'title': x['title'], 'id': x['tconst']}  for x in imdb.top_250()[:number_of_films]]
    titles_and_plots = [{'title': x['title'], 'plot': imdb.find_movie_by_id(x['id']).plot['outline'] } for x in titles_and_ids]
    titles_and_tokens = {x['title']: list(set(x['plot'].split())) for x in titles_and_plots}
    return json.dumps(titles_and_tokens)

if __name__ == '__main__':
    import sys
    print get_documents(2)
