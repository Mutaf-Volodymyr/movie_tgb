from sqlalchemy import MetaData, Table, select, and_
from sarch_moduls.sakila_conection import MySQLReader

class SearchMovieByCategory(MySQLReader):
    def __init__(self, *, user, password, host, database):
        super().__init__(user=user, password=password, host=host, database=database)
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

    def add_new_category_to_search(self, id, category):
        self.choices_categories[id] = category

    def add_new_year_to_search(self, year:int):
        self.choices_years.add(year)

    def add_all_category_to_search(self):
        for id, category in self.get_all_category():
            self.add_new_category_to_search(int(id), category)

    def add_many_years_to_search(self, start, end):
        self.choices_years.update(range(start, end+1))

    def search_movie_by_category_and_years(self):
        try:
            metadata = MetaData()

            film = Table(self.film_table, metadata, autoload_with=self.engine)
            film_category = Table(self.film_category_table, metadata, autoload_with=self.engine)

            query = select(film.c.film_id, film.c.title) \
                .select_from(
                film.join(film_category, film.c.film_id == film_category.c.film_id))\
                .where(and_(
                    film_category.c.category_id.in_(self.choices_categories.keys()),
                    film.c.release_year.in_(self.choices_years))).limit(10)

            with self.engine.connect() as connection:
                results = connection.execute(query)
                return results.fetchall()
        except Exception as e:
            print(f" Error reading data from table'{self.film_table}': {e}")
            return []

