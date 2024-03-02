from aiogram import  Router, types
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from Messages.message_text import start_message ,On_start_button , project_option_text , Succeed_payment_VIP_Signals , Succeed_Free_Signals
from Keyboards.keyboard import start_keyboard , project_option_keyboard
from aiogram.types import CallbackQuery 
from Keyboards.keyboard_classes import StartClass , ProjectOptionClass
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from Support_Utils.imports import bot
from aiogram.methods.create_chat_invite_link import CreateChatInviteLink
from datetime import datetime, timedelta
import time


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

@router.message(StateFilter("get_user_id"))
async def getting_user(message:Message , state:FSMContext)->None:
    await state.clear()
    # The user id will be getted from user and will be checked through the API
    user_id = message.text
    keyboard = await project_option_keyboard()
    await message.answer(text=project_option_text , reply_markup=keyboard)

@router.callback_query(ProjectOptionClass.filter(F.btn_purpose == "vip_subscription"))
async def vip_subscription(query:types.CallbackQuery,callback_data  , state:FSMContext)->None:
    await state.clear()
    # channel_username = -1002026717052
    # chat = await bot.get_chat(chat_id=channel_username)
    # user_id = query.from_user.id
    # print(user_id)
    # await bot.add_chat_member(chat_id=chat.id, user_id=user_id)
    # channel_username = "vipsinglas8project"
    # invite_link = f"https://t.me/{channel_username}?joinchat=" + await bot.get_chat_invite_link(channel_username)
    # print(invite_link)
    # chat_invite_link = "https://t.me/+zCl1iThmLj1jYjVk"
    ChatInviteLink = await bot(CreateChatInviteLink(chat_id="-1002026717052", name="vipsinglas8project" , expire_date=int(time.time() + 86400) , member_limit = 1) )
    invite_link = ChatInviteLink.invite_link
    await query.message.answer(text=f"{invite_link} \n {Succeed_payment_VIP_Signals}" )
    await query.answer()


@router.callback_query(ProjectOptionClass.filter(F.btn_purpose == "free_subscription"))
async def free_subscription(query:types.CallbackQuery , callback_data , state:FSMContext)->None:
    await state.clear()
    free_invite_link = "https://t.me/+MYUgaX3SuWVhNmMx"
    await query.message.answer(text = f"Invitation LINK = {free_invite_link} \n {Succeed_Free_Signals}")
    await query.answer()




    

