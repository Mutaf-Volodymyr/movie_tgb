from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class Film(Base):
    __tablename__ = 'film'
    film_id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    release_year = Column(Integer)
    rating = Column(String)
    categories = relationship("FilmCategory", back_populates="film")
    actors = relationship("FilmActor", back_populates="film")

class Category(Base):
    __tablename__ = 'category'
    category_id = Column(Integer, primary_key=True)
    name = Column(String)
    films = relationship("FilmCategory", back_populates="category")

class FilmCategory(Base):
    __tablename__ = 'film_category'
    film_id = Column(Integer, ForeignKey('film.film_id'), primary_key=True)
    category_id = Column(Integer, ForeignKey('category.category_id'), )
    film = relationship("Film", back_populates="categories")
    category = relationship("Category", back_populates="films")

class Actor(Base):
    __tablename__ = 'actor'
    actor_id = Column(Integer, primary_key=True)
    name = Column(String)
    films = relationship("FilmActor", back_populates="actor")

class FilmActor(Base):
    __tablename__ = 'film_actor'
    film_id = Column(Integer, ForeignKey('film.film_id'), primary_key=True)
    actor_id = Column(Integer, ForeignKey('actor.actor_id'))
    film = relationship("Film", back_populates="actors")
    actor = relationship("Actor", back_populates="films")




# film = session.query(Film).filter_by(film_id=1).one()
# for film_category in film.categories:
#     print(film_category.category.name)


# category = session.query(Category).filter_by(category_id=1).one()
# for film_category in category.films:
#     print(film_category.film.title)