import sqlite3

def create_db_users():
    with sqlite3.connect('users.db') as conn:
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS users (
                    `id` int auto_increment primary key,
                    `name` varchar(20),
                    `surname` varchar(20), 
                    `craeted_at` timestamp
                    )''')
        conn.commit()

        cur.execute('''CREATE TABLE IF NOT EXISTS searches (
                    `id` int auto_increment primary key,
                    `user_id` int not null,
                    `film_id` int not null,
                    `craeted_at` timestamp,
                    foreign key (user_id) references users(id)
                    )''')




if __name__ == '__main__':
    create_db_users()