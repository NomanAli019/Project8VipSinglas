from aiogram.methods.send_message import SendMessage
from Support_Utils.imports import bot
import time
from Database.user_db_operation import get_users

async def get_all_check_user():
    while True:
        time.sleep(5)
        all_user = await get_users()
        # user_id_list = []
        if all_user:
            for i in all_user:
                await bot(SendMessage(chat_id=i.chat_id , text="hello you just got registered!!"))
        else:
            print(" user no found ")      
        