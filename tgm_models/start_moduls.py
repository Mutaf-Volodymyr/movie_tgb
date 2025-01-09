from .bot_init import bot
from .write_function import create_new_user

from .search_actors_models import search_actors
from .popular_moduls import show_popular
from .search_title_models import search_movie_by_title
from .search_category_models import search_by_category

from telebot import types

@bot.message_handler(commands=['start'])
def start(message):
    user_name = message.from_user.first_name
    create_new_user(message)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = [
        types.KeyboardButton('Search by title'),
        types.KeyboardButton('Search by category and years'),
        types.KeyboardButton('Search by actors'),
        types.KeyboardButton('Show popular')
    ]
    markup.row(*buttons[:2])
    markup.row(*buttons[2:])
    bot.send_message(
        message.chat.id,
        f"Hello {user_name}, welcome! Please choose an option:",
        reply_markup=markup
    )


@bot.message_handler(
    func=lambda message: message.text in ['Search by title', 'Search by category and years', 'Show popular',
                                          'Search by actors'])
def handle_buttons(message):
    match message.text:
        case 'Search by category and years':
            bot.send_message(message.chat.id, "<b>What categories do you like?</b>", parse_mode='html')
            search_by_category(message)
        case 'Search by title':
            bot.send_message(message.chat.id, "<b>Please enter the movie title you want to search for:</b>",
                             parse_mode='html')
            bot.register_next_step_handler(message, search_movie_by_title)
        case 'Search by actors':
            bot.send_message(message.chat.id, "<b>Please enter the name of actors:</b>",
                             parse_mode='html')
            bot.register_next_step_handler(message, search_actors)
        case 'Show popular':
            show_popular(message)