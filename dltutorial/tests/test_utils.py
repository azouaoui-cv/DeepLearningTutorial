"""
Unit testing utility functions in utils.py

Creation date: 2018/04/10

Author: Alexandre Zouaoui @inzouzouwetrust
"""
# Utilities packages
from os import path
import logging
import os

# Movies database API packages
import tmdbsimple as tmdb
import imdb

# Custom utility functions to be tested
from dltutorial.utils import get_movie_id_tmdb
from dltutorial.utils import get_movie_info_tmdb
from dltutorial.utils import get_movie_genres_tmdb
from dltutorial.utils import get_api_key_tmdb

from dltutorial.utils import get_movie_info_imdb
from dltutorial.utils import get_movie_genres_imdb



def test_utils_tmdb(test_movie_name="The Matrix"):
    """
    Unit testing tmdb utility functions
    
    Parameters
    --------------
    - test_movie_name : string (optional)
        Movie name on which tests are run.
        By default: 'The Matrix'
        
    Returns
    --------------
    None (used by pytest)
    """
    
    # Retrieving API Key
    api_key = get_api_key_tmdb(main_folder=path.abspath('./dltutorial/'))
    # Assert non null API Key
    assert len(api_key) > 0
    # Set the TMDB API key
    tmdb.API_KEY = api_key 
    logging.debug('TMDB API key is set to %s...' % api_key)

    # Instanciate a search object from TMDB
    search_tmdb = tmdb.Search()

    # Unit tests
    movie_id = get_movie_id_tmdb(test_movie_name, search_tmdb=search_tmdb)
    assert isinstance(movie_id, int)
    movie_info = get_movie_info_tmdb(test_movie_name, search_tmdb=search_tmdb)
    assert isinstance(movie_info, dict)
    movie_genres = get_movie_genres_tmdb(test_movie_name, search_tmdb=search_tmdb)
    assert isinstance(movie_genres, list)

def test_utils_imdb(test_movie_name="The Matrix"):
    """
    Unit testing imdb utility functions
    
    Parameters
    --------------
    - test_movie_name : string (optional)
        Movie name on which tests are run.
        By default: 'The Matrix'
        
    Returns
    --------------
    None (used by pytest)
    """ 
    
    # Instanciate a search object from IMDB
    search_imdb = imdb.IMDb()
    
    # Unit tests
    movie_genres = get_movie_genres_imdb(movie_name=movie_name, search_imdb=search_imdb)
    assert isinstance(movie_genres, list)
    movie_info = get_movie_info_imdb(movie_name=movie_name, search_imdb=search_imdb)
    assert isinstance(movie_info, imdb.Movie.Movie)
