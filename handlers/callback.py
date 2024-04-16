from aiogram import  Router, types
from aiogram.filters import CommandStart 
from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from Messages.message_text import start_message ,On_start_button , project_option_vip_subs_msg , free_subscription_msg , get_started_subs , Succeed_payment_VIP_Signals , Succeed_Free_Signals , ready_to_subs_40 , ready_to_subs_30 , cancel_subs_confirm
from Keyboards.keyboard import start_keyboard , project_option_keyboard , Vip_subscription_option
from aiogram.types import CallbackQuery 
from Keyboards.keyboard_classes import StartClass , ProjectOptionClass , MenuClass , CancelSubscribeClass
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from Support_Utils.imports import bot
from aiogram.methods.create_chat_invite_link import CreateChatInviteLink
from datetime import datetime, timedelta
import time
from Keyboards.join_link_keyboard import invite_link_keyboard , free_invite_link_keyboard
from Database.user_db_operation import check_user , add_user , get_user_data
from Database.subscription_operation import get_user_subscription_data , add_subscription , check_user_subscription , update_subscriptions
from Database.payment_db_operation import add_payment , check_payment , update_payment
from aiogram.methods.ban_chat_member import BanChatMember 
from aiogram.methods.unban_chat_member import UnbanChatMember
from aiogram.methods.send_video import SendVideo
from Messages.message_text import how_to_set_chart_url , how_to_p8_signal , already_have_subs
from Keyboards.Menu_keyboard import subs_menu_keyboard
from Database.stripe_customer_record import check_stripe_customer , add_stripe_customer , delete_customer
from Keyboards.subscribe_keyboard import subscriber_button
from Database.user_remainder_db_op import add_reminder , delete_reminder
from Database.stripe_customer_record import get_customer_record , delete_customer
from aiogram.methods.delete_message import DeleteMessage
from Database.promo_code_db_op import add_user_promo_code_status , get_promo_code
from Keyboards.cancel_sub_keyboard import cancel_sub_option
from Database.user_db_operation import update_user_promo_code_status , update_user_customer_id , update_user_sub_status
import stripe
router = Router()
import os
# enter the stripe api 
STRIPE_API = os.getenv("Stripe_api_key")
stripe.api_key = STRIPE_API

# @router.message()
# async def echo_handler(message:types.Message)->None:
#     await message.answer("Command Not found!")

@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    get_start_button = await start_keyboard()
    photo_url = "https://www.jotform.com/uploads/projecteigh8/form_files/ppp-02.65b1c99d58b658.78272717.jpg"
    await message.answer_photo(photo=photo_url, caption=start_message, reply_markup=get_start_button)

# promo code callback 
@router.callback_query(StartClass.filter(F.btn_name == "start_button"))
async def promo_code(query:types.CallbackQuery , callback_data , state:FSMContext):
    
    try:        
        user_data = await check_user(query.from_user.id)
        if user_data:
            keyboard = await project_option_keyboard()
            title_msg1 = """
Project 8 has two options to choose from:

1️⃣ Project 8 Subscription Model:"""
            title_msg2 = """2️⃣ Project 8 FREE Model"""
            await query.message.answer(text=f"{hbold(title_msg1)}  \n  {project_option_vip_subs_msg}" )
            await query.message.answer(text=f"{hbold(title_msg2)}  \n  {free_subscription_msg}" )
            await query.message.answer(text=get_started_subs , reply_markup=keyboard )
        else:
            raise ValueError

    except Exception as e:
        await state.clear()
        Enter_id = types.ForceReply(input_field_placeholder="Enter Promo Code .......")
        await query.message.answer(text="Enter Promo Code " , reply_markup=Enter_id)
        await query.answer()
        await state.set_state("get_promo_code")
    
    await query.answer()

# getting promo code 
@router.message(StateFilter("get_promo_code"))
async def getting_user_promo_code(message:Message , state:FSMContext)->None:
    try:
        promo_code = int(message.text)
        promo_code_size = len(str(promo_code))
        if promo_code_size != 6:
            raise ValueError
        else:
            photo_url = "https://innotechsol.com/getuser_id_Guide_pic.png"
            Enter_id = types.ForceReply(input_field_placeholder="Enter Your ID .......")
            user = await check_user(message.from_user.id)
            if user:
                keyboard = await project_option_keyboard()
                title_msg1 = """
        Project 8 has two options to choose from:

        1️⃣ Project 8 Subscription Model:"""
                title_msg2 = """2️⃣ Project 8 FREE Model"""
                await message.answer(text=f"{hbold(title_msg1)}  \n  {project_option_vip_subs_msg}" )
                await message.answer(text=f"{hbold(title_msg2)}  \n  {free_subscription_msg}" )
                await message.answer(text=get_started_subs , reply_markup=keyboard )
            else:
                await state.clear()
                await message.answer_photo(photo=photo_url , caption=On_start_button , reply_markup=Enter_id)
                
                await state.set_data({"promo_code" : promo_code})
                await state.set_state("get_user_id")

            # await state.clear()
            # await state.set_state("pocket_option_account")
            # await state.set_data({"promo_code" : promo_code})



    except Exception as e:
        get_start_button = await start_keyboard()
        await message.answer(text="The Promo Code must be a 6 digit Integer " , reply_markup=get_start_button)
        await state.clear()
        



# @router.message(StateFilter("pocket_option_account"))
# async def start_button(message:Message , state:FSMContext):
#     code = await state.get_data()
#     promo_code = code["promo_code"]
#     photo_url = "https://innotechsol.com/getuser_id_Guide_pic.png"
#     Enter_id = types.ForceReply(input_field_placeholder="Enter Your ID .......")
#     user = await check_user(message.from_user.id)
#     if user:
#         keyboard = await project_option_keyboard()
#         title_msg1 = """
# Project 8 has two options to choose from:

# 1️⃣ Project 8 Subscription Model:"""
#         title_msg2 = """2️⃣ Project 8 FREE Model"""
#         await message.answer(text=f"{hbold(title_msg1)}  \n  {project_option_vip_subs_msg}" )
#         await message.answer(text=f"{hbold(title_msg2)}  \n  {free_subscription_msg}" )
#         await message.answer(text=get_started_subs , reply_markup=keyboard )
#     else:
#         await state.clear()
#         await message.answer_photo(photo=photo_url , caption=On_start_button , reply_markup=Enter_id)
#         await message.answer()
#         await state.set_state("get_user_id")
#         await state.set_data({"promo_code" : promo_code})
        
        # await state.set_data({"message_id":query.message.message_id})
    # await state.set_data({"query" : query})

@router.message(StateFilter("get_user_id"))
async def getting_user(message:Message , state:FSMContext)->None:
    
    # The user id will be getted from user and will be checked through the API
    code = await state.get_data()
    promo_code = code["promo_code"]
    try:
        pocket_option_id = int(message.text)
        pocket_op_id_size = len(str(pocket_option_id))
        print(pocket_op_id_size)
        if pocket_op_id_size != 8:
            raise ValueError
        print(message.from_user.username)
        user = await check_user(message.from_user.id)
        if user == False:
            if message.from_user.username:
                await add_user(message.from_user.id , pocket_option_id , message.from_user.username , promo_code , "NO Value" , "NO Value" , "NO Value")
                if promo_code == 786786:
                    await add_user_promo_code_status(message.from_user.id , "Active")
                    await update_user_promo_code_status(message.from_user.id , "Active")
                    # giving you free subscription for 30 days
                    current_time = datetime.now()
                    new_datetime = current_time + timedelta(days=30)
                    await add_payment(message.from_user.id  , message.from_user.username , "Activate")
                    await add_subscription(message.from_user.id ,new_datetime , "Premium" )
                    time.sleep(2)
                    await bot(UnbanChatMember(chat_id="-1002097584929" , user_id=message.from_user.id))
                    ChatInviteLink = await bot(CreateChatInviteLink(chat_id="-1002097584929", name="vipsinglas8project" , expire_date=int(time.time() + 86400) , member_limit = 1) )
                    invite_link = ChatInviteLink.invite_link
                    keyboard = await invite_link_keyboard(invite_link)
                    await message.answer(text=f" You Activated Promo code and get 30 days free subscription of VIP channel. \n After this we will charge you 30$/Month " , reply_markup=keyboard)
                    time.sleep(2)
                    video1_path = how_to_set_chart_url
                    await bot(SendVideo(chat_id=message.from_user.id , video=video1_path , caption="How To Set Up Your Charts"))
                    video2_path = how_to_p8_signal
                    await bot(SendVideo(chat_id=message.from_user.id , video=video2_path , caption="How to execute the Project 8 Trades"))
                    time.sleep(5)
                    await state.clear()
                    # payment_state = await check_payment(message.from_user.id)
    #                 menu_keyboard = await subs_menu_keyboard()
    #                 await message.answer(f"""```
    # Subscriber User Name: {message.from_user.username} 
    # Subscription Status : {payment_state.payment_status}```""" , reply_markup=menu_keyboard , parse_mode="MARKDOWNV2")
                        


                else:
                    await add_user_promo_code_status(message.from_user.id , "Expired")
                    await update_user_promo_code_status(message.from_user.id , "Expired")
            else:
                await add_user(message.from_user.id , pocket_option_id , str(message.from_user.id) , promo_code)
                if promo_code == 786786:
                    await add_user_promo_code_status(message.from_user.id , "Active")
                    await update_user_promo_code_status(message.from_user.id , "Active")
                    # giving you free subscription for 30 days 
                    current_time = datetime.now()
                    new_datetime = current_time + timedelta(days=30)
                    await add_payment(message.from_user.id  , str(message.from_user.id) , "Activate")
                    await add_subscription(message.from_user.id ,new_datetime , "Premium" )
                    time.sleep(2)
                    await bot(UnbanChatMember(chat_id="-1002097584929" , user_id=message.from_user.id))
                    ChatInviteLink = await bot(CreateChatInviteLink(chat_id="-1002097584929", name="vipsinglas8project" , expire_date=int(time.time() + 86400) , member_limit = 1) )
                    invite_link = ChatInviteLink.invite_link
                    keyboard = await invite_link_keyboard(invite_link)
                    await message.answer(text=f" You Activated Promo code and get 30 days free subscription of VIP channel. \n After this we will charge you 30$/Month  " , reply_markup=keyboard)
                    time.sleep(2)
                    video1_path = how_to_set_chart_url
                    await bot(SendVideo(chat_id=message.from_user.id , video=video1_path , caption="How To Set Up Your Charts"))
                    video2_path = how_to_p8_signal
                    await bot(SendVideo(chat_id=message.from_user.id , video=video2_path , caption="How to execute the Project 8 Trades"))
                    time.sleep(5)
                    await state.clear()
    #                 payment_state = await check_payment(message.from_user.id)
    #                 menu_keyboard = await subs_menu_keyboard()
    #                 await message.answer(f"""```
    # Subscriber User Name: {message.from_user.id} 
    # Subscription Status : {payment_state.payment_status}```""" , reply_markup=menu_keyboard , parse_mode="MARKDOWNV2")

                else:
                    await add_user_promo_code_status(message.from_user.id , "Expired")
                    await update_user_promo_code_status(message.from_user.id , "Expired")
        if promo_code != 786786:
            keyboard = await project_option_keyboard()
            title_msg1 = """
        Project 8 has two options to choose from:

        1️⃣ Project 8 Subscription Model:"""
            title_msg2 = """2️⃣ Project 8 FREE Model"""
            await message.answer(text=f"{hbold(title_msg1)}  \n  {project_option_vip_subs_msg}" )
            await message.answer(text=f"{hbold(title_msg2)}  \n  {free_subscription_msg}" )
            await message.answer(text=get_started_subs , reply_markup=keyboard )
            await state.clear()
    except Exception as e:
        print(e)
        get_start_button = await start_keyboard()
        await message.answer(text="The Pocket Option Account Id Size and pattern is not right Please Try Again" , reply_markup=get_start_button)
        await state.clear()
    


@router.callback_query(ProjectOptionClass.filter(F.btn_purpose == "vip_subscription"))
async def vip_subscription(query:types.CallbackQuery,callback_data  , state:FSMContext)->None:
    await state.clear()
    keyboard = await Vip_subscription_option()
    try:
        subs = await get_user_subscription_data(query.from_user.id)
        user = await get_user_data(query.from_user.id)
        if subs:
            payment_state = await check_payment(query.from_user.id)
            if payment_state.payment_status == "Deactivate":
                
                if user.promo_code == 786786:
                    await query.message.answer(text=ready_to_subs_30 , reply_markup=keyboard)
                else:
                    await query.message.answer(text=ready_to_subs_40 , reply_markup=keyboard)
            else:
                await query.answer(text=already_have_subs)
        else:
            if user.promo_code == 786786:
                await query.message.answer(text=ready_to_subs_30 , reply_markup=keyboard)
            else:
                await query.message.answer(text=ready_to_subs_40 , reply_markup=keyboard)
    except Exception as e:
        if user.promo_code == 786786:
            await query.message.answer(text=ready_to_subs_30 , reply_markup=keyboard)
        else:
            await query.message.answer(text=ready_to_subs_40 , reply_markup=keyboard)

    await query.answer()
    await state.clear()

@router.callback_query(ProjectOptionClass.filter(F.btn_purpose == "No_vip_subscription"))
async def no_vip_subscription(query:types.CallbackQuery,callback_data , state:FSMContext)->None:
    await state.clear()
    await bot.delete_message(chat_id=query.message.chat.id , message_id=query.message.message_id)
    await query.message.answer("Subscription process canceled.")
    await query.answer()

@router.callback_query(ProjectOptionClass.filter(F.btn_purpose == "Yes_vip_subscription"))
async def yesvip_subscription(query:types.CallbackQuery,callback_data  , state:FSMContext)->None:
    await state.clear()

    
    
    customer_record = await check_stripe_customer(query.from_user.id)
    if customer_record == False:

        

        
        subs = await get_user_subscription_data(query.from_user.id)
    #     if subs:
    #         payment_state = await check_payment(query.from_user.id)
    #         if payment_state.payment_status == "Deactivate":
    #             current_time = datetime.now()
    #             # how to add 30 days 
    #             # new_datetime = current_time + timedelta(days=30)
    #             new_datetime = current_time + timedelta(days=30)
    #             await update_subscription(query.from_user.id , new_datetime)
    #             await update_payment(query.from_user.id , "Activate")
    #             await bot(UnbanChatMember(chat_id="-1002026717052" , user_id=subs.user_id))
    #             ChatInviteLink = await bot(CreateChatInviteLink(chat_id="-1002026717052", name="vipsinglas8project" , expire_date=int(time.time() + 86400) , member_limit = 1) )
    #             invite_link = ChatInviteLink.invite_link
    #             keyboard = await invite_link_keyboard(invite_link)
    #             await query.message.answer(text=f" {Succeed_payment_VIP_Signals}" , reply_markup=keyboard)
    #             time.sleep(5)
    #             keyboard = await subs_menu_keyboard()
    #             await query.message.answer(f"""```
    # Subscriber User Name: {query.from_user.username} 
    # Subscription Status : {payment_state.payment_status}```""" , reply_markup=keyboard , parse_mode="MARKDOWNV2")
            

        if subs == False:
            if query.from_user.username:
                new_customer = stripe.Customer.create(
                email=query.from_user.username+"@gmail.com",
                description=f"Customer: {query.from_user.username}")
            else:
                user_id_tostr = str(query.from_user.id)
                new_customer = stripe.Customer.create(
                email=user_id_tostr+"@gmail.com",
                description=f"Customer: {query.from_user.username}")

            


            
            user = await get_user_data(query.from_user.id) 
            if user.promo_code == 786786:
                # 40 dollar per month subscription product price id  ok
                price_id = 'price_1OxaDQECJwpMr51i8Agz2NVs'
            else:
                # 30 dollar per month subscription product price id  ok
                price_id = 'price_1OqHAoEBIZzPqApbhtCSWPbQ'
                            
            session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            customer=new_customer.id,
            line_items=[
                {
                    "price": price_id,
                    "quantity": 1,
                }
            ],
            mode="subscription",
            success_url="https://innotechsol.com/success.html",  # Replace with your success URL
            cancel_url="https://innotechsol.com/failure.html"  # Replace with your cancel URL
            )
            
            subscribe_button_keyboard = await subscriber_button(session.url)

            await query.message.answer(text="Click the button and compelete the Transaction within 5 minutes " , reply_markup=subscribe_button_keyboard)
            await query.message.answer(text="Poccessing Transaction  . . . . . . . ")
            start_time = time.time()
            duration = 5 * 60
            while (time.time() - start_time) < duration:
                ret_session = stripe.checkout.Session.retrieve(session.id)
                payment_status = ret_session.payment_status
                if payment_status == "paid":
                    break
                
            if payment_status == "paid":
                
                await add_stripe_customer(query.from_user.id , new_customer.id)
                await add_reminder(query.from_user.id , "Open")

                current_time = datetime.now()
                new_datetime = current_time + timedelta(days=30)
                if query.from_user.username:
                    await add_payment(query.from_user.id  , query.from_user.username , "Activate")
                else:
                    await add_payment(query.from_user.id  , str(query.from_user.id) , "Activate")
                await add_subscription(query.from_user.id ,new_datetime , "Premium" )

                await update_user_customer_id(query.from_user.id , new_customer.id)
                await update_user_sub_status(query.from_user.id , "Activate")
                

                
                time.sleep(2)
                await bot(UnbanChatMember(chat_id="-1002097584929" , user_id=query.from_user.id))
                ChatInviteLink = await bot(CreateChatInviteLink(chat_id="-1002097584929", name="vipsinglas8project" , expire_date=int(time.time() + 86400) , member_limit = 1) )
                invite_link = ChatInviteLink.invite_link
                keyboard = await invite_link_keyboard(invite_link)
                await query.message.answer(text=f" {Succeed_payment_VIP_Signals}" , reply_markup=keyboard)
                time.sleep(2)
                video1_path = how_to_set_chart_url
                await bot(SendVideo(chat_id=query.from_user.id , video=video1_path , caption="How To Set Up Your Charts"))
                video2_path = how_to_p8_signal
                await bot(SendVideo(chat_id=query.from_user.id , video=video2_path , caption="How to execute the Project 8 Trades"))
                time.sleep(5)
                payment_state = await check_payment(query.from_user.id)
                menu_keyboard = await subs_menu_keyboard()
                await query.message.answer(f"""```
Subscriber User Name: {query.from_user.username} 
Subscription Status : {payment_state.payment_status}```""" , reply_markup=menu_keyboard , parse_mode="MARKDOWNV2")
            else:
                stripe.Customer.delete(
                    new_customer.id
                )
                await query.message.answer(text="Transaction Time Over ")

        else:
            await query.message.answer("Your Already have Active subscription!")

    else:
        print("the customer and his subscription already exists")

    



@router.callback_query(ProjectOptionClass.filter(F.btn_purpose == "free_subscription"))
async def free_subscription(query:types.CallbackQuery , callback_data , state:FSMContext)->None:
    await state.clear()
    free_invite_link = "https://t.me/+kRv4Pa9qrqZmZDUx"
    keyboard =  await free_invite_link_keyboard(free_invite_link)
    await query.message.answer(text = f"{Succeed_Free_Signals}" , reply_markup=keyboard)
    await query.answer()



@router.message(Command("menu"))
async def menu(message: Message, state: FSMContext):
    try:
        payment_state = await check_payment(message.from_user.id)
        username = message.from_user.username
        if payment_state:
            menu_keyboard = await subs_menu_keyboard()
            if username:
                await message.answer(f"""```
    Subscriber User Name: {message.from_user.username} 
    Subscription Status : {payment_state.payment_status}```""" , reply_markup=menu_keyboard , parse_mode="MARKDOWNV2")
            else:
                await message.answer(f"""```
    Subscriber User Name: {message.from_user.id}
    Subscription Status : {payment_state.payment_status}```""" , reply_markup=menu_keyboard , parse_mode="MARKDOWNV2")
        else:
            await message.answer("You Cannot Access Menu Because You Do Not Have A Subscription Yet!!!")
    except Exception as e:
        await message.answer("You Cannot Access Menu Because You Do Not Have A Subscription Yet!!!")


@router.callback_query(MenuClass.filter(F.btn_purpose == "cancel_subscription"))
async def cancel_subscription(query:types.CallbackQuery , callback_data , state:FSMContext):
   
   keyboard = await cancel_sub_option()
   await query.message.answer(cancel_subs_confirm , reply_markup=keyboard)

@router.callback_query(CancelSubscribeClass.filter(F.btn_type == "yes"))
async def cancel_sub_yes(query:types.CallbackQuery , callback_data , state:FSMContext):
    
    try:
        customer = await get_customer_record(query.from_user.id)
        subscriptions = stripe.Subscription.list(customer=customer.stripe_cus_id)
        for subscription in subscriptions.auto_paging_iter():
            try:
                subscription = stripe.Subscription.delete(subscription.id)
                await query.message.answer(f"Subscription ID: {subscription.id} cancelled successfully!")

            except stripe.error.StripeError as e:
                await query.message.answer("Error cancelling subscription:", e)
    except Exception as e:
        await query.message.answer(f"ERROR! ")
    
    await query.answer()

@router.callback_query(CancelSubscribeClass.filter(F.btn_type == "no"))
async def cancel_sub_no(query:types.CallbackQuery , callback_data , state:FSMContext):
    await bot.delete_message(chat_id=query.message.chat.id , message_id=query.message.message_id)
    await query.message.answer("Subscription Cancellation Operation Canceled")
    await query.answer()