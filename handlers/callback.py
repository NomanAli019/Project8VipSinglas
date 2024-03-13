from aiogram import  Router, types
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from Messages.message_text import start_message ,On_start_button , project_option_text , Succeed_payment_VIP_Signals , Succeed_Free_Signals
from Keyboards.keyboard import start_keyboard , project_option_keyboard , Vip_subscription_option
from aiogram.types import CallbackQuery 
from Keyboards.keyboard_classes import StartClass , ProjectOptionClass
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from Support_Utils.imports import bot
from aiogram.methods.create_chat_invite_link import CreateChatInviteLink
from datetime import datetime, timedelta
import time
from Keyboards.join_link_keyboard import invite_link_keyboard , free_invite_link_keyboard
from Database.user_db_operation import check_user , add_user
from Database.subscription_operation import get_user_subscription_data , add_subscription , check_user_subscription , update_subscription
from Database.payment_db_operation import add_payment , check_payment , update_payment
from aiogram.methods.ban_chat_member import BanChatMember 
from aiogram.methods.unban_chat_member import UnbanChatMember
from aiogram.methods.send_video import SendVideo
import youtube_dl
router = Router()

@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    get_start_button = await start_keyboard()
    photo_url = "https://www.jotform.com/uploads/projecteigh8/form_files/ppp-02.65b1c99d58b658.78272717.jpg"
    await message.answer_photo(photo=photo_url, caption=start_message, reply_markup=get_start_button)


@router.callback_query(StartClass.filter(F.btn_name=="start_button"))
async def start_button(query:types.CallbackQuery,callback_data , state: FSMContext):
    photo_url = "https://assets.bwbx.io/images/users/iqjWHBFdfxIU/iavN7.giIZDs/v1/-1x-1.jpg"
    Enter_id = types.ForceReply(input_field_placeholder="Enter Your ID .......")
    await query.message.answer_photo(photo=photo_url , caption=On_start_button , reply_markup=Enter_id)
    await query.answer()
    await state.set_state("get_user_id")
    # await state.set_data({"query" : query})

@router.message(StateFilter("get_user_id"))
async def getting_user(message:Message , state:FSMContext)->None:
    
    # The user id will be getted from user and will be checked through the API
    # query = await state.get_data()
    pocket_option_id = message.text
    print(message.from_user.username)
    user = await check_user(message.from_user.id)
    if user == False:
        await add_user(message.from_user.id , pocket_option_id , message.from_user.username)
    keyboard = await project_option_keyboard()
    await message.answer(text=project_option_text , reply_markup=keyboard)
    await state.clear()

@router.callback_query(ProjectOptionClass.filter(F.btn_purpose == "vip_subscription"))
async def vip_subscription(query:types.CallbackQuery,callback_data  , state:FSMContext)->None:
    await state.clear()
    keyboard = await Vip_subscription_option()
    
    await query.message.answer(text="Ready to Subscribe $30/Month cancel anytime  from the menu tab " , reply_markup=keyboard)
    
    await query.answer()

@router.callback_query(ProjectOptionClass.filter(F.btn_purpose == "Yes_vip_subscription"))
async def yesvip_subscription(query:types.CallbackQuery,callback_data  , state:FSMContext)->None:
    await state.clear()
    await query.message.answer(text="Payment URL:  https://dashboard.stripe.com/login")
    await query.message.answer(text="Poccessing Transaction  . . . . . . . ")
    subs = await get_user_subscription_data(query.from_user.id)
    if subs:
        payment_state = await check_payment(query.from_user.id)
        if payment_state.payment_status == "Deactivate":
            await update_payment(query.from_user.id , "Activate")
            current_time = datetime.now()
            new_datetime = current_time + timedelta(minutes=2)
            await update_subscription(query.from_user.id , new_datetime)
            await bot(UnbanChatMember(chat_id="-1002026717052" , user_id=subs.user_id))
            ChatInviteLink = await bot(CreateChatInviteLink(chat_id="-1002026717052", name="vipsinglas8project" , expire_date=int(time.time() + 86400) , member_limit = 1) )
            invite_link = ChatInviteLink.invite_link
            keyboard = await invite_link_keyboard(invite_link)
            await query.message.answer(text=f" {Succeed_payment_VIP_Signals}" , reply_markup=keyboard)

    else:
        current_time = datetime.now()
        new_datetime = current_time + timedelta(minutes=2)
        await add_payment(query.from_user.id  , query.from_user.username , "Activate")
        await add_subscription(query.from_user.id ,new_datetime , "Premium" )
        
        
        time.sleep(2)
        await bot(UnbanChatMember(chat_id="-1002026717052" , user_id=query.from_user.id))
        ChatInviteLink = await bot(CreateChatInviteLink(chat_id="-1002026717052", name="vipsinglas8project" , expire_date=int(time.time() + 86400) , member_limit = 1) )
        invite_link = ChatInviteLink.invite_link
        keyboard = await invite_link_keyboard(invite_link)
        await query.message.answer(text=f" {Succeed_payment_VIP_Signals}" , reply_markup=keyboard)

        
        # video_path = "C:\project8telegrambot\charts.mp4"
        # await bot.send_video(chat_id=query.from_user.id , video=open(video_path, "rb"))
        
        # await bot(SendVideo(chat_id=query.from_user.id , video=how_to_set_chart_url))

    # while True:
    #     subscriber_data = await get_user_subscription_data(query.from_user.id) 
    #     user_subscription_time = subscriber_data.subs_time
    #     current_time = datetime.now()
    #     if current_time > user_subscription_time:
    #         await bot(BanChatMember(chat_id="-1002026717052" , user_id=subscriber_data.user_id))
    #         await update_payment(query.from_user.id , "Deactivate")
    #         await query.message.answer("Subscription time is  over we banned you from channel !!")
    #         break
    #     time.sleep(10)
    



@router.callback_query(ProjectOptionClass.filter(F.btn_purpose == "free_subscription"))
async def free_subscription(query:types.CallbackQuery , callback_data , state:FSMContext)->None:
    await state.clear()
    free_invite_link = "https://t.me/+MYUgaX3SuWVhNmMx"
    keyboard =  await free_invite_link_keyboard(free_invite_link)
    await query.message.answer(text = f"{Succeed_Free_Signals}" , reply_markup=keyboard)
    await query.answer()




    

