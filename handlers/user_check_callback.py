import asyncio
import threading
from datetime import datetime , timedelta
from aiogram import Bot
from aiogram.methods.send_message import SendMessage
from aiogram.methods.ban_chat_member import BanChatMember
from Database.subscription_operation import get_all_subscriber , delete_subscription
from Database.payment_db_operation import update_payment, check_payment , delete_payment
from Support_Utils.imports import TOKEN  # Replace with your actual bot_token
from Database.user_remainder_db_op import check_reminder , delete_reminder , add_reminder 
from Database.stripe_customer_record import get_customer_record , delete_customer
from Database.promo_code_db_op import get_promo_code , update_promo_code
import time
import stripe 
import os 
stripe.api_key = os.getenv("Stripe_api_key")

# async def update_subscription():
#     while True:
#         subscriber_data = await get_all_subscriber()
#         print("update subscriber ")
#         try:
#             for i in subscriber_data:
#                 user_subscription_time = i.subs_time
#                 current_time = datetime.now()
#                 if current_time > user_subscription_time + timedelta(minutes=120):
#                     customer = await get_customer_record(i.user_id)
#                     try:
#                         subscriptions = stripe.Subscription.list(customer=customer.stripe_cus_id)
#                         for subscription in subscriptions.auto_paging_iter():
#                             payment_status = subscription.status

#                             # Process payment based on status
#                             if payment_status == "active":
#                                 current_time = datetime.now()
#                                 # how to add 30 days 
#                                 new_datetime = current_time + timedelta(days=30)
#                                 await add_reminder(i.user_id , "Open")
#                                 await update_subscription(i.user_id , new_datetime)
#                                 await update_payment(i.user_id , "Activate")
#                                 # Customer has paid
#                                 print(f"Subscription ID: {subscription.id} - Payment Successful!")
#                             else:
#                                 # Handle other statuses (unpaid, past_due, etc.)
#                                 print(f"Subscription ID: {subscription.id} - Payment Status: {payment_status}")

#                     except stripe.error.StripeError as e:
#                         print("Error retrieving subscriptions:")
#         except Exception as e:
#             time.sleep(15)




async def get_all_check_user(bot: Bot):
    while True:
        try:
            subscriber_data = await get_all_subscriber()
            for i in subscriber_data:
                getting_payment = await check_payment(i.user_id)
                if getting_payment.payment_status == "Activate":
                    user_subscription_time = i.subs_time
                    current_time = datetime.now()
                    reminder_time = user_subscription_time - timedelta(days=5)
                    reminder = await check_reminder(i.user_id)
                    if reminder:
                        if current_time > reminder_time:
                            await bot.send_message(i.user_id, "Last 5 days Remaing of Your Subscription!")
                            await delete_reminder(i.user_id)
                    else:
                        if current_time > user_subscription_time + timedelta(days=1):
                            await bot.send_message(i.user_id, "We banned you from the channel Your Subscription Time is over!")
                            await bot.ban_chat_member(chat_id="-1002093844830", user_id=i.user_id)
                            await delete_payment(i.user_id)
                            await delete_subscription(i.user_id)
                            await delete_customer(i.user_id)
                            promo_code_data = await get_promo_code(i.user_id)
                            if promo_code_data:
                                if promo_code_data.promo_code_status == "Active":
                                    await update_promo_code(i.user_id , "Expired")


                                

                                

        except Exception as e:
            time.sleep(15)



def run_user_check():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    bot_instance = Bot(token=TOKEN)  # Replace bot_token with your actual bot token
    # tasks = [
    #     get_all_check_user(bot_instance),
    #     update_subscription()
    # ]
    loop.run_until_complete(get_all_check_user(bot_instance))

if __name__ == "__main__":
    user_check_thread = threading.Thread(target=run_user_check)
    user_check_thread.start()
