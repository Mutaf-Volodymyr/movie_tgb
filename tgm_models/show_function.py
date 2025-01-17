from telebot import types
from .bot_init import bot
from .write_function import db_counter_one
from db_sqlite_manager import all_table
from db_sqlite_manager import DatabaseSQLiteManager, engine_sqlite
from db_sakila_manager import SearchMovieByTitle, engine_sakila


def show_movis(message, reader):
    titles_films = reader.fetch_title()
    if not titles_films:
        bot.send_message(message.chat.id, "Sorry, no movies found.")
    else:
        markup = types.InlineKeyboardMarkup()
        for id, title in titles_films:
            markup.add(types.InlineKeyboardButton(f'{title}', callback_data=f'film_id: {id}'))
        bot.send_message(message.chat.id, "Choose a movie:", reply_markup=markup)

        if len(titles_films) == reader.limit:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(f'...search more', callback_data=f'search_more'))
            bot.send_message(message.chat.id, "Try search next movie", reply_markup=markup)

            @bot.callback_query_handler(func=lambda call: call.data == "search_more")
            def search_more(callback):
                reader.change_offset()
                show_movis(message, reader)


def get_popular(table_name):
    if table_name not in all_table:
        raise ValueError(f"Table {table_name} not found.")

    model = all_table[table_name]
    with DatabaseSQLiteManager(engine_sqlite) as db_manager:
        record_ids = db_manager.query(model.id).order_by(model.counter.desc()).limit(5).all()
        return [record_id[0] for record_id in record_ids]




@bot.callback_query_handler(func=lambda call: call.data.startswith("film_id: "))
def get_info_about_movie(callback):
    movie_id = int(callback.data[9:])
    db_counter_one(movie_id, 'popular_films')
    reader = SearchMovieByTitle(engine_sakila)

    info = reader.get_info_about_film(movie_id)
    bot.send_message(callback.message.chat.id, info, parse_mode='html')
