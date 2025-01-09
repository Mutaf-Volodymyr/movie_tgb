from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    nickname = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (UniqueConstraint(
        'name', 'surname', 'nickname', name='_name_surname_nickname_uc'),
    )

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', surname='{self.surname}', created_at='{self.created_at}')>"


class PopularActors(Base):
    __tablename__ = 'popular_actors'

    id = Column(Integer, primary_key=True)
    counter = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<PopularActors(id={self.id}, actor_id='{self.actor_id}, counter='{self.counter}'"


class PopularFilms(Base):
    __tablename__ = 'popular_films'

    id = Column(Integer, primary_key=True)
    counter = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<PopularActor(id={self.id}, film_id='{self.film_id}, counter='{self.counter}'"


class PopularCategories(Base):
    __tablename__ = 'popular_categories'

    id = Column(Integer, primary_key=True)
    counter = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<PopularActor(id={self.id}, film_id='{self.film_id}, counter='{self.counter}'"


all_table = {
        'popular_films': PopularFilms,
        'popular_actors': PopularActors,
        'popular_categories': PopularCategories
    }