from .bot_init import bot
from telebot import types
from db_sakila_manager import SearchMovieByTitle, SearchMovieByActors, SearchMovieByCategory, engine_sakila
from .show_function import get_popular


@bot.callback_query_handler(func=lambda call: call.data.startswith("popular_"))
def popular_button(callback):
    ids = get_popular(callback.data)
    match callback.data:
        case 'popular_actors':
            reader_popular = SearchMovieByActors(engine_sakila)
        case 'popular_categories':
            reader_popular = SearchMovieByCategory(engine_sakila)
        case 'popular_films':
            reader_popular = SearchMovieByTitle(engine_sakila)
    bot.send_message(callback.message.chat.id, reader_popular.get_popular(ids))


def show_popular(message):
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton(f'actors', callback_data=f'popular_actors'),
        types.InlineKeyboardButton(f'categories', callback_data=f'popular_categories'),
        types.InlineKeyboardButton(f'film', callback_data=f'popular_films')
    )
    bot.send_message(message.chat.id, "Make a choice:", reply_markup=markup)



