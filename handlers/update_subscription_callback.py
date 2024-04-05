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
from Database.user_db_operation import update_user_promo_code_status , update_user_customer_id , update_user_sub_status
from Database.subscription_operation import update_subscriptions
import time
import stripe 
import os 
stripe.api_key = os.getenv("Stripe_api_key")

async def update_subscription(bot: Bot):
    while True:
        subscriber_data = await get_all_subscriber()
       
        try:
            # print("hello in update")
            for i in subscriber_data:
                user_subscription_time = i.subs_time
                current_time = datetime.now()
                if current_time > user_subscription_time :
                    customer = await get_customer_record(i.user_id)
                    try:
                        subscriptions = stripe.Subscription.list(customer=customer.stripe_cus_id)
                        for subscription in subscriptions.auto_paging_iter():
                            payment_status = subscription.status

                            # Process payment based on status
                            if payment_status == "active":
                                current_time = datetime.now()
                                # how to add 30 days 
                                new_datetime = current_time + timedelta(days=30)
                                await add_reminder(i.user_id , "Open")
                                await update_subscriptions(i.user_id , new_datetime)
                                await update_payment(i.user_id , "Activate")
                                await update_user_sub_status(i.user_id , "Activate")
                                # Customer has paid
                                await bot.send_message(i.user_id, "Your Subcription Time is Updated !")
                                print(f"Subscription ID: {subscription.id} - Payment Successful!")
                            else:
                                # Handle other statuses (unpaid, past_due, etc.)
                                print(f"Subscription ID: {subscription.id} - Payment Status: {payment_status}")

                    except stripe.error.StripeError as e:
                        print("Error retrieving subscriptions:")
        except Exception as e:
            time.sleep(15)


def update_user_sub():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    bot_instance = Bot(token=TOKEN)  # Replace bot_token with your actual bot token
  
    loop.run_until_complete(update_subscription(bot_instance))

if __name__ == "__main__":
    user_check_thread = threading.Thread(target=update_user_sub)
    user_check_thread.start()