from telebot import types
from re import findall
from db_sakila_manager import SearchMovieByTitle, engine_sakila, SearchMovieByCategory, SearchMovieByActors
from tgm_models import bot, create_new_user, db_counter_one, db_counter_many, show_movis, get_popular



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

def show_popular(message):
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton(f'actors', callback_data=f'popular_actors'),
        types.InlineKeyboardButton(f'categories', callback_data=f'popular_categories'),
        types.InlineKeyboardButton(f'film', callback_data=f'popular_films')
    )
    bot.send_message(message.chat.id, "Make a choice:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("popular_"))
def popular_button(callback):
    ids = get_popular(callback.data)
    match callback.data:
        case 'popular_actors':
            reader_popular = SearchMovieByActors(engine_sakila)
            bot.send_message(callback.message.chat.id, reader_popular.get_popular(ids))
        case 'popular_categories':
            reader_popular = SearchMovieByCategory(engine_sakila)
        case 'popular_films':
            reader_popular = SearchMovieByTitle(engine_sakila)
    bot.send_message(callback.message.chat.id, reader_popular.get_popular(ids))

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


def search_by_category(message):
    for_delete_message = None
    reader = SearchMovieByCategory(engine_sakila)
    # reader.reset_obj()
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
        nonlocal for_delete_message
        end_message = "<b>Write the year diapason:</b>\n    For example: 1995 - 1999\n<b>Or one year:</b>\n    For example: 1995"
        if callback.data.startswith("category_id: "):
            id, category = callback.data.split(": ")[1].split('@')
            reader.add_or_del_new_category_to_search(int(id), category)
            if for_delete_message:
                bot.delete_message(message.chat.id, for_delete_message.message_id)
            for_delete_message = bot.send_message(message.chat.id, f"Categories selected: {', '.join(reader.choices_categories.values())}")
        elif callback.data == "Doesnt_matter":
            reader.add_all_category_to_search()
            bot.send_message(callback.message.chat.id, end_message, parse_mode='html')
            bot.register_next_step_handler(callback.message, add_years)
        elif callback.data == "Finish_selection":
            db_counter_many(reader.get_choices_categories_id(), 'popular_categories')
            bot.send_message(callback.message.chat.id, end_message, parse_mode='html')
            bot.register_next_step_handler(callback.message, add_years)

    def add_years(message):
        user_years: str = message.text.strip()
        try:
            date = sorted(map(int, (findall(r'\d{4}', user_years))))
            if len(date) == 1:
                reader.add_one_year_to_search(*date)
            elif len(date) == 2:
                reader.add_many_years_to_search(*date)
            else:
                raise ValueError
            show_movis(message, reader)
        except ValueError as e:
            bot.send_message(message.chat.id, "Wrong input. Try agen", parse_mode='html')
            bot.register_next_step_handler(message, add_years)


def search_movie_by_title(message):
    choices_titles: str = message.text.strip()
    bot.send_message(message.chat.id, f"Searching for movies...")
    reader = SearchMovieByTitle(engine_sakila)
    reader.set_new_choice_titles(choices_titles)
    show_movis(message, reader)


@bot.callback_query_handler(func=lambda call: call.data.startswith("film_id: "))
def get_info_about_movie(callback):
    movie_id = int(callback.data[9:])
    db_counter_one(movie_id, 'popular_films')
    reader = SearchMovieByTitle(engine_sakila)

    info = reader.get_info_about_film(movie_id)
    bot.send_message(callback.message.chat.id, info, parse_mode='html')


if __name__ == '__main__':
    bot.polling(none_stop=True)
