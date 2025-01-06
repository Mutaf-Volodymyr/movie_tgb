from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

class DatabaseManager:
    def __init__(self):
        self.engine = create_engine('sqlite:///../users.db')
        self.Session = sessionmaker(bind=self.engine)
        self.session = None

    def __enter__(self):
        self.session = self.Session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            self.session.close()

    def get_session(self):
        return self.session






