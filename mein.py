import telebot
from telebot import types
import os
import dotenv
from pathlib import Path
from re import fullmatch
from sarch_moduls.search_movie_by_title import SearchMovieByTitle
from sarch_moduls.show_popular_movie import ShowPopularMovie, GetPopularMovie
from sarch_moduls.search_movie_by_category import SearchMovieByCategory
from write_moduls.write_new_user import UserManager
from write_moduls.sqllite_conection import DatabaseManager


dotenv.load_dotenv(Path('.env'))
bot = telebot.TeleBot(os.environ.get('token'))

dbconfig = {'host': os.environ.get('host'),
            'user': os.environ.get('user'),
            'password': os.environ.get('password'),
            'database': os.environ.get('database')}


@bot.message_handler(commands=['start'])
def start(message):
    user_name = message.from_user.first_name
    user_surname = message.from_user.surname
    create_new_user(user_name, user_surname)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = [
        types.KeyboardButton('Search by title'),
        types.KeyboardButton('Search by category and years'),
        types.KeyboardButton('Show popular movies')
    ]
    markup.row(*buttons[:2])
    markup.row(*buttons[2:])
    bot.send_message(
        message.chat.id,
        f"Hello {user_name}, welcome! Please choose an option:",
        reply_markup=markup
    )


@bot.message_handler(func=lambda message: message.text in ['Search by title', 'Search by category and years', 'Show popular movies'])
def handle_buttons(message):
    match message.text:
        case 'Search by category and years':
            bot.send_message(message.chat.id, "<b>What categories do you like?</b>", parse_mode='html')
            search_by_category(message)
        case 'Search by title':
            bot.send_message(message.chat.id, "<b>Please enter the movie title you want to search for:</b>", parse_mode='html')
            bot.register_next_step_handler(message, search_movie_by_title)
        case 'Show popular movies':
            bot.register_next_step_handler(message, search_popular_search)


def search_by_category(message):
    reader = SearchMovieByCategory(**dbconfig) # BUG IS HEAR <----------------------
    reader.reset_obj()
    reader.connect()
    categories = reader.get_all_category()
    markup = types.InlineKeyboardMarkup()
    row = []
    for id, category in categories:
        row.append(types.InlineKeyboardButton(f'{category}', callback_data=f'category_id: {id}@{category}'))
        if len(row) == 2:
            markup.row(*row)
            row = []
    if row:
        markup.row(*row)
    markup.add(types.InlineKeyboardButton(f'Finish selection', callback_data='Finish_selection'))
    markup.add(types.InlineKeyboardButton(f"Doesn't matter", callback_data="Doesnt_matter"))
    bot.send_message(message.chat.id, "Choose a categories:", reply_markup=markup)

    @bot.callback_query_handler(
        func=lambda call: call.data.startswith("category_id: ") or call.data in ('Finish_selection', "Doesnt_matter"))
    def add_chose(callback):
        if callback.data.startswith("category_id: "):
            id, category = callback.data.split(": ")[1].split('@')
            reader.add_new_category_to_search(int(id), category)
            bot.send_message(message.chat.id, f"Categories selected: {', '.join(reader.choices_categories.values())}")
        elif callback.data == "Doesnt_matter":
            reader.add_all_category_to_search()
            bot.send_message(callback.message.chat.id, "<b>Specify the year range. For example: 1995-1999</b>",
                             parse_mode='html')
            bot.register_next_step_handler(callback.message, add_years)
        elif callback.data == "Finish_selection":
            bot.send_message(callback.message.chat.id, "<b>Specify the year range. For example: 1995-1999</b>",
                             parse_mode='html')
            bot.register_next_step_handler(callback.message, add_years)

    def add_years(message):
        user_years: str = message.text.strip()
        if fullmatch(r'\d{4}-\d{4}', user_years):
            start, end = map(int, user_years.split('-'))
            reader.add_many_years_to_search(start, end)
            show_movis(message, reader)
        else:
            pass # доработать !!!!!

def search_movie_by_title(message):
    choices_titles: str = message.text.strip()
    bot.send_message(message.chat.id, f"Searching for movies...")
    reader = SearchMovieByTitle(**dbconfig)
    reader.set_new_choice_titles(choices_titles)
    reader.connect()
    show_movis(message, reader)


def show_movis(message, reader):
    titles_films = reader.fetch_title()
    if not titles_films:
        bot.send_message(message.chat.id, "Sorry, no movies found.")
    else:
        markup = types.InlineKeyboardMarkup()
        for id, title in titles_films:
            markup.add(types.InlineKeyboardButton(f'{title}', callback_data=f'film_id: {id}'))
        bot.send_message(message.chat.id, "Choose a movie:", reply_markup=markup)
        if  titles_films == reader.limit:
            markup.add(types.InlineKeyboardButton(f'...search more', callback_data=f'...search more'))

            @bot.callback_query_handler(func=lambda call: call.data =="..search more")
            def search_more(callback):
                reader.change_offset()
                show_movis(message, reader)



@bot.callback_query_handler(func=lambda call: call.data.startswith("film_id: "))
def get_info_about_movie(callback):
    movie_id = int(callback.data[9:])
    reader = SearchMovieByTitle(**dbconfig)
    reader.connect()
    info = reader.show_info_about_film(movie_id)
    bot.send_message(callback.message.chat.id, info, parse_mode='html')


def search_popular_search(message):
    reader = GetPopularMovie(SQLITE_URL)
    reader.connect()
    id_list = reader.search_most_popular_film()
    reader = ShowPopularMovie(**dbconfig)
    reader.connect()
    titles_films = reader.get_some_films(id_list)
    show_movis(message, titles_films)


def create_new_user(name, surname):
    with DatabaseManager() as db_manager:
        user_manager = UserManager(db_manager)
        user_manager.add_user(name, surname)


# Error adding user: (sqlite3.OperationalError) no such table: users
# [SQL: INSERT INTO users (name, surname) VALUES (?, ?)]
# [parameters: ('Владимир', 'Мутаф')]


if __name__ == '__main__':
    bot.polling(none_stop=True)
