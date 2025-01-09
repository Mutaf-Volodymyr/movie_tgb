from .bot_init import bot
from .write_function import db_counter_one
from telebot import types
from db_sakila_manager import SearchMovieByActors, engine_sakila
from .show_function import show_movis


def search_actors(message):
    choices_actors: str = message.text.strip()
    reader = SearchMovieByActors(engine_sakila)
    reader.set_new_choice_actors(choices_actors)
    actors = reader.fetch_actors()
    if actors:
        markup = types.InlineKeyboardMarkup()
        for id, full_name_actors in actors:
            markup.add(types.InlineKeyboardButton(f'{full_name_actors}', callback_data=f'actor_id: {id}'))
        bot.send_message(message.chat.id, "Choose a actors to get all films with this actors:", reply_markup=markup)
    else:
        pass

    @bot.callback_query_handler(
        func=lambda call: call.data.startswith("actor_id: "))
    def get_actor(callback):
        actor_id = int(callback.data[10:])
        db_counter_one(actor_id, 'popular_actors')
        reader.set_actor_id(actor_id)
        show_movis(message, reader)