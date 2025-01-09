from db_sqlite_manager import DatabaseSQLiteManager, engine_sqlite, Base, UserManager
from db_sqlite_manager import all_table

def create_new_user(massage):
    name = massage.from_user.first_name
    surname = massage.from_user.last_name
    nickname = massage.from_user.username
    with DatabaseSQLiteManager(engine_sqlite) as db_manager:
        Base.metadata.create_all(engine_sqlite)
        user_manager = UserManager(db_manager)
        user_manager.add_user(name, surname, nickname)


def db_counter_one(id: int, table_name: str):
    if table_name not in all_table:
        raise ValueError(f"Table {table_name} not found.")

    model = all_table[table_name]

    with DatabaseSQLiteManager(engine_sqlite) as db_manager:
        record = db_manager.query(model).filter(model.id == id).first()
        if record:
            record.counter += 1
        else:
            new_record = model(id=id, counter=1)
            db_manager.add(new_record)

        db_manager.commit()


def db_counter_many(ids: [int], table_name: str):
    for id in ids:
        db_counter_one(id, table_name)