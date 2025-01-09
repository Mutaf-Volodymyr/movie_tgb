from sqlalchemy import create_engine
from .sqllite_conection import DatabaseSQLiteManager
from .user_manager import UserManager
from pathlib import Path
from .table_models import (
    Base,
    User,
    PopularFilms,
    PopularActors,
    PopularCategories,
    all_table
)

current_directory = Path.cwd()
parent_directory = current_directory

try:
    engine_sqlite = create_engine(
        url=f'sqlite:///{parent_directory}/DB_for_tgb.db',
        echo=True,  # For testing
        pool_size=5,
        max_overflow=10
    )
except Exception as e:
    print('SQLite Engine not create: ', e)
