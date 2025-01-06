from sqlalchemy import MetaData, Table, select
from sarch_moduls.sakila_conection import MySQLReader

class SearchMovieByTitle(MySQLReader):
    def __init__(self, *, user, password, host, database):
        super().__init__(user=user, password=password, host=host, database=database)
        self.choice_titles = None

    def set_new_choice_titles(self, new_title: str):
        self.choice_titles = new_title.upper()

    def fetch_title(self):
        try:
            metadata = MetaData()
            table = Table(self.film_table, metadata, autoload_with=self.engine)
            query = select(table.c.film_id, table.c.title)\
                .where(table.c.title.ilike(f"%{self.choice_titles}%"))\
                .limit(self.limit).offset(self.offset)


            with self.engine.connect() as connection:
                results = connection.execute(query)
                return results.fetchall()
        except Exception as e:
            print(f"Error reading data from table '{self.film_table}': {e}")
            return []



