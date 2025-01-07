from sqlalchemy import MetaData, Table, select, func
from sarch_moduls.sakila_conection import MySQLReader


class SearchMovieByActors(MySQLReader):
    def __init__(self, *, user, password, host, database):
        super().__init__(user=user, password=password, host=host, database=database)
        self.choice_actors = None
        self.actor_id = None

    def set_new_choice_actors(self, new_actors: str):
        self.choice_actors = new_actors.upper()

    def set_actor_id(self, actor_id: int):
        self.actor_id = actor_id

    def fetch_actors(self):
        try:
            metadata = MetaData()
            table = Table(self.actor_table, metadata, autoload_with=self.engine)
            full_name = func.concat(table.c.first_name, ' ', table.c.last_name)
            query = (
                select(table.c.actor_id, full_name.label("full_name"))
                    .where(full_name.ilike(f"%{self.choice_actors}%"))
                    .limit(self.limit)
                    .offset(self.offset)
            )

            with self.engine.connect() as connection:
                results = connection.execute(query)
                return results.fetchall()
        except Exception as e:
            print(f"Error reading data from table '{self.film_table}': {e}")
            return []

    def fetch_title(self):
        try:
            metadata = MetaData()

            film_actor_table = Table(self.film_actor_table, metadata, autoload_with=self.engine)
            film_table = Table(self.film_table, metadata, autoload_with=self.engine)

            query = (
                select(film_table.c.film_id, film_table.c.title)
                .select_from(
                    film_actor_table.join(film_table, film_actor_table.c.film_id == film_table.c.film_id)
                )
                .where(film_actor_table.c.actor_id == self.actor_id).limit(self.limit).offset(self.offset)
            )

            with self.engine.connect() as connection:
                results = connection.execute(query)
                return results.fetchall()

        except Exception as e:
            print(f"Error reading data from join('{self.film_table}, {self.film_actor_table})': {e}")
            return []
