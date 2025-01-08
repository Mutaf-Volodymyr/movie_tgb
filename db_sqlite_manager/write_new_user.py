from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'main'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', surname='{self.surname}', created_at='{self.created_at}')>"


class UserManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def add_user(self, name, surname):
        try:
            new_user = User(name=name, surname=surname)
            self.db_manager.add(new_user)
            self.db_manager.commit()
        except Exception as e:
            self.db_manager.rollback()
            print(f"Error adding user: {e}")

    def get_all_users(self):
        try:
            users = self.db_manager.session.query(User).all()
            return users
        except Exception as e:
            print(f"Error getting users: {e}")
            return []

