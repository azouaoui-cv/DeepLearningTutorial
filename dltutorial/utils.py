"""
Utility functions used in the main notebooks.

Updates:
- 2018/04/10: includes TMDB utility functions.
    - get_movie_poster_tmdb
    - get_movie_id_tmdb
    - get_movie_info_tmdb
    - get_movie_genres_tmdb
    
Creation date: 2018/04/10

Author: Alexandre Zouaoui @inzouzouwetrust
"""

### Imports ###
# Web access packages
import wget

# Utilities packages
import os
from os import path
import logging

# Movies database API packages
import tmdbsimple as tmdb
import imdb

def get_api_key_tmdb(main_folder='./'):
    """
    Retrieve TMDB API Key
    
    Parameters
    ----------
    - main_folder :
        folder where to search the private subfolder
    
    
    Returns
    ----------
    api_key : string
        Null if no api_key found.
    """

    logging.info('Setting TMDB API key...')
    abs_path = path.abspath(main_folder)
    if 'private' in os.listdir(abs_path):
        logging.debug('Private folder exists...')
        from dltutorial import private
        api_key = private.API_KEY
    else:
        logging.debug('No private folder found in %s...' % abs_path)
        print('There is no private folder in %s.'
              'API key will remain blank if you do not set it in'
              ' dltutorial/utils.py' % abs_path)
        api_key = '' # put your own API key but do not share it
    return api_key


def get_movie_poster_tmdb(movie_name, search_tmdb, path):
    """
    Download a movie poster from TMDB using the movie name.
    
    Parameters
    -----------
    - movie_name : string
        Name of the movie
    
    - search_tmdb : tmdb.Search object
        tmdb instantiated Search object
        
    - path : string
        path where to store the results
        
    Returns
    ----------
    1:
        if the poster gets properly downloaded by the OS command
    """
    
    logging.debug('Searching movie %s in TMDB...' % movie_name)
    # Response from TMDB API search object
    response = search_tmdb.movie(query=movie_name)
    # Getting movie ID
    movie_id = response['results'][0]['id']
    # Getting movie info
    movie_info = tmdb.Movies(movie_id)
    # Getting movie poster path
    poster_path = movie_info.info()['poster_path']
    # Getting movie title
    movie_title = movie_info.info()['original_title']
    # Setting url to be downloaded
    url = 'image.tmdb.org/t/p/original' + poster_path
    logging.debug('URL to get downloaded %s...' % url)
    # Renaming title with underscores
    movie_title = '_'.join(movie_title.split(' '))
    # Setting wget download command
    strcmd = 'wget -O '+ path + movie_title + '.jpg ' + url
    # Executing command
    logging.debug('wget command to be executed %s...' % strcmd)
    os.system(strcmd)
    return 1

def get_movie_id_tmdb(movie_name, search_tmdb):
    """
    Get movie ID from TMDB API using the movie name
    
    Parameters
    -----------
    - movie_name : string
        Name of the movie
        
    - search_tmdb : tmdb.Search object
        tmdb instantiated Search object
        
    Returns
    ----------
    - movie_id : integer
        ID of the movie in TMDB
    """
    # Response from TMDB API search object
    logging.debug('Searching movie %s in TMDB...' % movie_name)
    response = search_tmdb.movie(query=movie_name)
    # Getting movie ID
    movie_id = response['results'][0]['id']
    logging.debug('Movie id (%s) from movie %s' %
                 (movie_id, movie_name))
    return movie_id

def get_movie_info_tmdb(movie_name, search_tmdb):
    """
    Get movie info from TMDB using movie name
    
    Parameters
    -----------
    - movie_name : string
        Name of the movie
        
    - search_tmdb : tmdb.Search object
        tmdb instantiated Search object
        
    Returns
    ----------
    - movie_info : dictionary
        dictionary containing movie info
    """
    
    logging.debug('Searching movie %s in TMDB...' % movie_name)
    # Response from TMDB API search object
    response = search_tmdb.movie(query=movie_name)
    # Getting movie id
    movie_id = response['results'][0]['id']
    # Getting movie info from id
    movie_info = tmdb.Movies(movie_id).info()
    logging.debug('Movie info retrieved? %s...' % (movie_info is not None))
    return movie_info

def get_movie_genres_tmdb(movie_name, search_tmdb):
    """
    Get movie genres from TMDB using movie name
    
    Parameters
    -----------
    - movie_name : string
        Name of the movie
        
    - search_tmdb : tmdb.Search object
        tmdb instantiated Search object
        
    Returns
    ----------
    - movie_genres : list of dictionaries
        dictionaries list containing movie genres
    """
    
    logging.debug('Searching movie %s in TMDB...' % movie_name)
    # Response from TMDB API search object
    response = search_tmdb.movie(query=movie_name)
    # Getting movie ID
    movie_id = response['results'][0]['id']
    # Getting movie genres from movie info
    movie_genres = tmdb.Movies(movie_id).info()['genres']
    logging.debug('Movie genres retrieved %s...' % movie_genres)
    return movie_genres

def get_movie_genres_imdb(movie_name, search_imdb):
    """
    Get movie genres from IMDB using movie name
    
    Parameters
    -----------
    - movie_name : string
        Name of the movie
        
    - search_imdb : imdb.IMDb object
        imdb instantiated object
        
    Returns
    ----------
    - movie_genres : list of strings
        strings list containing movie genres
    """
    logging.debug("Search movie %s in IMDB..." % movie_name)
    # Search and retrieve first result
    movie_info = search_imdb.search_movie(movie_name)[0]
    # Enrich movie infos
    search_imdb.update(movie_info)
    # Extract movie genres
    movie_genres = movie_info['genres']
    logging.debug("Retrieving movie genres %s..." % movie_genres)
    return movie_genres

def get_movie_info_imdb(movie_name, search_imdb):
    """
    Get movie infos from IMDB using movie name
    
    Parameters
    -----------
    - movie_name : string
        Name of the movie
        
    - search_imdb : imdb.IMDb object
        imdb instantiated object
        
    Returns
    ----------
    - movie_info : dictionary
        dictionary containing movie infos
    """
    logging.debug("Search movie %s in IMDB..." % movie_name)
    # Search and retrieve first result
    movie_info = search_imdb.search_movie(movie_name)[0]
    # Enrich movie infos
    search_imdb.update(movie_info)
    logging.debug("Movie info retrieved? %s..." % (movie_info is not None))
    return movie_info

def custom_precision_recall(ground_truth, predictions):
    """
    Returns the precision and the recall of a prediction given 
    that we operate on multilabel-indicator labeling data
    
    Parameters
    -----------------
    - ground_truth : list of strings
        List of true genre strings
    
    - predictions : list of strings
        List of predicted genre strings
        
    Returns
    ------------------
    - precision : float
        Between 0 and 1
        Assess if a class is rightfully predicted
        whenever it is indeed the ground truth
        (i.e. P = TP / (TP + FP))
        
    - recall : float
        Between 0 and 1
        Assess if a class is only predicted when it
        is indeed the ground truth
        (i.e. R = TP / (TP + FN))
    """
    
    TP = 0
    FN = 0
    FP = 0
    logging.debug("Ground_truth is of size: %d" % len(ground_truth))
    logging.debug("Predictions is of size: %d" % len(predictions))
    assert len(ground_truth) == len(predictions)
    # Loop through ground truth
    for true_label in ground_truth:
        # Indeed predicted
        if true_label in predictions:
            TP += 1
        # Missed by prediction
        else:
            FN += 1
        
    # Loop through predictions
    for prediction in predictions:
        # What is predicted is missing in ground truth
        if prediction not in ground_truth:
            FP += 1
            
    precision = 0 if TP + FP == 0 else TP / float(TP + FP)
    recall = 0 if TP + FN == 0 else TP / float(TP + FN)
    
    return precision, recall