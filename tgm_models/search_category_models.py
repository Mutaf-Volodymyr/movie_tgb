from telebot import types
from re import findall
from db_sakila_manager import engine_sakila, SearchMovieByCategory
from .bot_init import bot
from .write_function import db_counter_many
from .show_function import show_movis



def search_by_category(message):
    for_delete_message = None
    global reader
    reader = SearchMovieByCategory(engine_sakila)
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
    markup.add(types.InlineKeyboardButton(f"Doesn't matter", callback_data="Doesnt_matter"))
    markup.add(types.InlineKeyboardButton(f"Clean all categories", callback_data="Clean all categories"))
    markup.add(types.InlineKeyboardButton(f'Finish selection', callback_data='Finish_selection'))
    bot.send_message(message.chat.id, "Choose a categories:", reply_markup=markup)

    @bot.callback_query_handler(
        func=lambda call: call.data.startswith("category_id: ") or call.data in ('Finish_selection', "Doesnt_matter", "Clean all categories"))
    def add_chose(callback):
        nonlocal for_delete_message
        end_message = "<b>Write the year diapason:</b>\nFor example: 1995 - 1999\n<b>Or one year:</b>\nFor example: 1995"
        if callback.data.startswith("category_id: "):
            id, category = callback.data.split(": ")[1].split('@')
            reader.add_or_del_new_category_to_search(int(id), category)
            if for_delete_message:
                bot.delete_message(message.chat.id, for_delete_message.message_id)
            for_delete_message = bot.send_message(message.chat.id,
                                                  f"Categories selected: {', '.join(reader.choices_categories.values())}")
        elif callback.data == "Clean all categories":
            reader.reset_obj()
            bot.delete_message(message.chat.id, for_delete_message.message_id)
            for_delete_message = bot.send_message(message.chat.id, "Categories is cleaning...")
        elif callback.data == "Doesnt_matter":
            reader.add_all_category_to_search()
            bot.send_message(callback.message.chat.id, end_message, parse_mode='html')
            bot.register_next_step_handler(callback.message, add_years)
        elif callback.data == "Finish_selection":
            if reader.choices_categories:
                db_counter_many(reader.get_choices_categories_id(), 'popular_categories')
                bot.send_message(callback.message.chat.id, end_message, parse_mode='html')
                bot.register_next_step_handler(callback.message, add_years)
            else:
                for_delete_message = bot.send_message(callback.message.chat.id, 'Select at least one category', parse_mode='html')

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
            reader.reset_obj()

        except ValueError as e:
            bot.send_message(message.chat.id, "Wrong input. Try agen", parse_mode='html')
            search_by_category(message)
