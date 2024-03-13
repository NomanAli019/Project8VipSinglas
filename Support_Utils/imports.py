from aiogram import Bot, Dispatcher, types, Router
from aiogram.enums import ParseMode
import time

from os import getenv
from dotenv import load_dotenv
import os
TOKEN = os.getenv("BOT_TOKEN")


bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
bot.send_message
dp = Dispatcher()