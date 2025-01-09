import os
import dotenv
from pathlib import Path
import telebot

dotenv.load_dotenv(Path('../.env'))
bot = telebot.TeleBot(os.environ.get('token'))
