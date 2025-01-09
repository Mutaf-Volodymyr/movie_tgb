from sqlalchemy import MetaData, Table, select, and_
from .sakila_conection import SakilaReader


class SearchMovieByCategory(SakilaReader):
    def __init__(self, engine):
        super().__init__(engine)
        self.choices_categories = dict()
        self.choices_years = set()

    def get_all_category(self):
        try:
            metadata = MetaData()
            table = Table(self.category_table, metadata, autoload_with=self.engine)
            query = select(table.c.category_id, table.c.name)
            with self.engine.connect() as connection:
                results = connection.execute(query)
                return results.fetchall()
        except Exception as e:
            print(f"Error reading data from table '{self.film_table}': {e}")
            return []

    def add_or_del_new_category_to_search(self, id, category):
        if id not in self.choices_categories:
            self.choices_categories[id] = category
        elif id in self.choices_categories:
            del self.choices_categories[id]

    def add_new_year_to_search(self, year: int):
        self.choices_years.add(year)

    def add_all_category_to_search(self):
        self.choices_categories = dict(self.get_all_category())

    def add_many_years_to_search(self, start, end):
        self.choices_years.update(range(start, end + 1))

    def add_one_year_to_search(self, year):
        self.choices_years.add(year)

    def reset_obj(self):
        self.choices_categories = dict()
        self.choices_years = set()
        self.limit = 10
        self.offset = 0

    def get_choices_categories_id(self):
        return self.choices_categories.keys()

    def fetch_title(self):
        try:
            metadata = MetaData()

            film = Table(self.film_table, metadata, autoload_with=self.engine)
            film_category = Table(self.film_category_table, metadata, autoload_with=self.engine)

            query = select(film.c.film_id, film.c.title) \
                .select_from(
                film.join(film_category, film.c.film_id == film_category.c.film_id)) \
                .where(and_(
                film_category.c.category_id.in_(self.choices_categories.keys()),
                film.c.release_year.in_(self.choices_years))).limit(self.limit).offset(self.offset)

            with self.engine.connect() as connection:
                results = connection.execute(query)
                return results.fetchall()
        except Exception as e:
            print(f" Error reading data from table'{self.film_table}': {e}")
            return []

    def get_popular(self, ids):
        try:
            metadata = MetaData()
            table = Table(self.category_table, metadata, autoload_with=self.engine)
            query = (
                select(table.c.name)
                .where(table.c.category_id.in_(ids)))

            with self.engine.connect() as connection:
                results = connection.execute(query)
                return 'CATEGORIES: \n' + ', '.join([i[0] for i in results.fetchall()])
        except Exception as e:
            print(f"Error reading data from table '{self.category_table}': {e}")
            return 'Sorry, there are no popular category 😥😥😥😥'