import asyncio
import threading
from datetime import datetime
from aiogram import Bot
from aiogram.methods.send_message import SendMessage
from aiogram.methods.ban_chat_member import BanChatMember
from Database.subscription_operation import get_all_subscriber
from Database.payment_db_operation import update_payment, check_payment
from Support_Utils.imports import TOKEN  # Replace with your actual bot_token
import time
async def get_all_check_user(bot: Bot):
    while True:
        try:
            subscriber_data = await get_all_subscriber()
            if subscriber_data:
                for i in subscriber_data:
                    getting_payment = await check_payment(i.user_id)
                    if getting_payment.payment_status == "Activate":
                        user_subscription_time = i.subs_time
                        current_time = datetime.now()

                        if current_time > user_subscription_time:
                            await bot.send_message(i.user_id, "Subscription time is over; you've been banned from the channel!")
                            await bot.ban_chat_member(chat_id="-1002026717052", user_id=i.user_id)
                            await update_payment(i.user_id, "Deactivate")
        except Exception as e:
            time.sleep(15)

def run_user_check():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    bot_instance = Bot(token=TOKEN)  # Replace bot_token with your actual bot token
    loop.run_until_complete(get_all_check_user(bot_instance))

if __name__ == "__main__":
    user_check_thread = threading.Thread(target=run_user_check)
    user_check_thread.start()
