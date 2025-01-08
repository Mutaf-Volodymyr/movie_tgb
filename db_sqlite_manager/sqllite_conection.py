from sqlalchemy.orm import sessionmaker

class DatabaseSQLiteManager:
    def __init__(self, engine):
        self.engine = engine
        self.Session = sessionmaker(bind=self.engine)
        self.session = None

    def __enter__(self):
        self.session = self.Session()
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()




# https://github.com/pareikoVladislav/190224_pydantic_sqlalchemy/blob/main/alchemy_queries/models.py







