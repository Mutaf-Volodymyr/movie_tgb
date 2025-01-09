from .bot_init import bot
from db_sakila_manager import SearchMovieByTitle, engine_sakila
from .show_function import show_movis


def search_movie_by_title(message):
    choices_titles: str = message.text.strip()
    bot.send_message(message.chat.id, f"Searching for movies...")
    reader = SearchMovieByTitle(engine_sakila)
    reader.set_new_choice_titles(choices_titles)
    show_movis(message, reader)

