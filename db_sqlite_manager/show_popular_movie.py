from sqlalchemy import create_engine, MetaData, Table, select, func, desc
from db_sakila_manager.sakila_conection import MySQLReader



class GetPopularMovie:
    def __init__(self, db_url:str):
        self.db_url = db_url
        self.engine = None
        self.users_table = 'users'
        self.searches_table = 'searches'

    def connect(self):
        try:
            self.engine = create_engine(self.db_url)
        except Exception as e:
            print(f"Error connecting to MySQL: {e}")

    def search_most_popular_film(self, limit:int = 3):
        try:
            metadata = MetaData()
            table = Table(self.searches_table, metadata, autoload_with=self.engine)
            query = select(table.c.film_id,func.sum(table.c.film_id).label('total')\
                    .group_by(table.c.film_id)\
                    .order_by(desc('total'))\
                    .limit(limit))
            with self.engine.connect() as connection:
                results = connection.execute(query).fetchall()
                return [i[0] for i in results]
        except Exception as e:
            print(f"Error reading data: {e}")



class ShowPopularMovie(MySQLReader):
    def __init__(self, *, user, password, host, database):
        super().__init__(user=user, password=password, host=host, database=database)

    def get_some_films(self, list_id: list[int]):
        try:
            metadata = MetaData()
            table = Table(self.film_table, metadata, autoload_with=self.engine)
            query = select(table.c.film_id, table.c.title)\
                .where(table.c.film_id.in_(list_id))
            with self.engine.connect() as connection:
                results = connection.execute(query)
                return results.fetchall()
        except Exception as e:
            print(f"Error reading data from table '{self.film_table}': {e}")
            return []

