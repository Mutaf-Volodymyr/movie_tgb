from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
import os
import dotenv
from pathlib import Path
from .sakila_conection import SakilaReader
from .search_movie_by_title import SearchMovieByTitle
from .search_movie_by_category import SearchMovieByCategory
from .search_movie_by_actors import SearchMovieByActors



dotenv.load_dotenv(Path('.env'))

dbconfig = {'host': os.environ.get('host'),
            'user': os.environ.get('user'),
            'password': os.environ.get('password'),
            'database': os.environ.get('database')}


try:
    engine_sakila = create_engine(
        url=f'mysql+pymysql://{dbconfig['user']}:{dbconfig['password']}@{dbconfig['host']}:3306/{dbconfig['database']}',
        echo=True, # For testing
        pool_size=5,
        max_overflow=10
    )
except Exception as e:
    print('Engine not create: ', e)


Base = declarative_base()