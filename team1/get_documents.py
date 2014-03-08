from imdbpie import Imdb
import json


imdb = Imdb({'anonymize': False})


def _tokenize_plot(plot):
    plot_words_unique = set(plot.split())
    # return as a list since python cant serialize
    # a set to JSON
    return list(plot_words_unique)


def _get_title_plot(top_movie):
    # Get the movie data from Imdb
    movie = imdb.find_movie_by_id(top_movie['tconst'])
    # Return the title and tokenized plot keyword list
    plot = movie.plot['outline']
    return movie.title, _tokenize_plot(plot)


def get_documents(number_of_movies=10):
    top_movies = imdb.top_250()[:number_of_movies]
    titles_and_tokens = dict([_get_title_plot(x) for x in top_movies])

    # return the final documents in json format for easy ingestion
    return json.dumps(titles_and_tokens)

if __name__ == '__main__':
    print get_documents()
