from aiogram import Bot, Dispatcher, types, Router
from aiogram.enums import ParseMode
import time

from os import getenv
from dotenv import load_dotenv
import os
TOKEN = "7144152895:AAERF3f5XMhRSKFdO3CiGCoXH3kANGwMvo4"


bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
bot.send_message
dp = Dispatcher()