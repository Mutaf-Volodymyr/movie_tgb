import telebot
from telebot import types
import os
import dotenv
from pathlib import Path
from sarch_moduls.search_movie_by_title import SearchMovieByTitle
from sarch_moduls.show_popular_movie import ShowPopularMovie, GetPopularMovie

dotenv.load_dotenv(Path('.env'))
bot = telebot.TeleBot(os.environ.get('token'))

dotenv.load_dotenv(Path('../.env'))
dbconfig = {'host': os.environ.get('host'),
            'user': os.environ.get('user'),
            'password': os.environ.get('password'),
            'database': os.environ.get('database')}

SQLITE_URL = 'sqlite:///../my_database.db'


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Search by movie name', callback_data='search_by_movie_name'))
    markup.add(types.InlineKeyboardButton('Search by category', callback_data='search_by_category'))
    markup.add(types.InlineKeyboardButton('Show popular movies', callback_data='show_popular'))
    user_name = message.from_user.first_name
    bot.send_message(message.chat.id, f"Hello {user_name}, welcome! Please choose an option:", reply_markup=markup)


@bot.callback_query_handler(
    func=lambda call: call.data in ['search_by_movie_name', 'search_by_category', 'show_popular'])
def callback_message(callback):
    match callback.data:
        case 'search_by_movie_name':
            bot.send_message(callback.message.chat.id, "Please enter the movie title you want to search for:")
            bot.register_next_step_handler(callback.message, search_movie_by_title)
        case 'Search by category':
            bot.send_message(callback.message.chat.id, "Please enter the category you want to search for:")
            bot.register_next_step_handler(callback.message, search_by_category)
        case 'Show popular movies':
            bot.register_next_step_handler(callback.message, search_popular_search)


@bot.message_handler(chat_types=['text'])
def search_movie_by_title(message):
    user_input: str = message.text.strip()
    bot.send_message(message.chat.id, f"Searching for movies...")
    reader = SearchMovieByTitle(**dbconfig)
    reader.connect()
    titles_films = reader.fetch_title(user_input)
    show_movis(message, titles_films)


def show_movis(message, titles_films):
    if titles_films:
        markup = types.InlineKeyboardMarkup()
        for id, title in titles_films:
            markup.add(types.InlineKeyboardButton(f'{title}', callback_data=f'id: {id}'))
        bot.send_message(message.chat.id, "Choose a movie:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Sorry, no movies found.")


@bot.callback_query_handler(func=lambda call: call.data.startswith("id: "))
def get_info_about_movie(callback):
    movie_id = int(callback.data[4:])
    reader = SearchMovieByTitle(**dbconfig)
    reader.connect()
    info = reader.show_info_about_film(movie_id)
    bot.send_message(callback.message.chat.id, info, parse_mode='html')


def search_by_category(message):
    pass


def search_popular_search(message):
    reader = GetPopularMovie(SQLITE_URL)
    reader.connect()
    id_list = reader.search_most_popular_film()
    reader = ShowPopularMovie(**dbconfig)
    reader.connect()
    titles_films = reader.get_some_films(id_list)
    show_movis(message, titles_films)


if __name__ == '__main__':
    bot.polling(none_stop=True)
