from sqlalchemy import MetaData, Table, select, func


class SakilaReader:
    def __init__(self, engine):
        self.engine = engine
        self.limit = 10
        self.offset = 0

        self.film_table = 'film'
        self.category_table = 'category'
        self.film_category_table = 'film_category'
        self.actor_table = 'actor'
        self.film_actor_table = 'film_actor'

    def change_offset(self):
        self.offset += self.limit

    def get_info_about_film(self, film_id):
        try:
            metadata = MetaData()

            film = Table(self.film_table, metadata, autoload_with=self.engine)
            film_category = Table(self.film_category_table, metadata, autoload_with=self.engine)
            category = Table(self.category_table, metadata, autoload_with=self.engine)
            actor = Table(self.actor_table, metadata, autoload_with=self.engine)
            film_actor = Table(self.film_actor_table, metadata, autoload_with=self.engine)

            query_film = select(film.c.title,
                           film.c.description,
                           film.c.rating,
                           film.c.release_year,
                           ).where(film.c.film_id == film_id)

            query_category = select(category.c.name)\
                            .select_from(category.join(film_category, film_category.c.category_id == category.c.category_id))\
                            .where(film_category.c.film_id == film_id)

            query_actors = select(func.concat(actor.c.last_name, ' ', actor.c.first_name))\
                            .select_from(actor.join(film_actor, actor.c.actor_id == film_actor.c.actor_id))\
                            .where(film_actor.c.film_id == film_id)


            with self.engine.connect() as connection:
                results = []
                results.append(connection.execute(query_film).fetchall()[0])
                results.append(connection.execute(query_category).fetchall())
                results.append(connection.execute(query_actors).fetchall())
                info = (f'<b>####### INFO ABOUT FILM #######</b>\n'
                        f'<b>TITLE:</b> {results[0][0]} ({results[0][3]})\n'
                        f'<b>CATEGORY:</b> {', '.join(map(lambda x: x[0], results[1]))}\n'
                        f'<b>RATING:</b> {results[0][2]}\n'
                        f'<b>DESCRIPTION:</b> {results[0][1]}\n'
                        f'<b>ACTORS:</b> {', '.join(map(lambda x: x[0], results[2]))}\n')
                return info

        except Exception as e:
            print(f"Error reading data: {e}")





