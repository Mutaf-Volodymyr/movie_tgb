from sqlalchemy import create_engine
from .sqllite_conection import DatabaseSQLiteManager
from .write_new_user import UserManager, User


try:
    engine_sqlite = create_engine(
        url=f'sqlite:///../DB_for_tgb.db',
        echo=True, # For testing
        pool_size=5,
        max_overflow=10
    )
except Exception as e:
    print('SQLite Engine not create: ', e)

