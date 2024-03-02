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


router = Router()

@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    get_start_button = await start_keyboard()
    photo_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTbgmNEUQSqr2a8yS2LfnWATl7Ps9ZCUJQZwE1CsjTq9g&s"
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
    # await message.answer(f"The User id = {user_id}")
    keyboard = await project_option_keyboard()
    await message.answer(text=project_option_text , reply_markup=keyboard)

@router.callback_query(ProjectOptionClass.filter(F.btn_purpose == "vip_subscription"))
async def vip_subscription(query:types.CallbackQuery,callback_data  , state:FSMContext)->None:
    await state.clear()
    await query.message.answer(text=Succeed_payment_VIP_Signals)
    await query.answer()


@router.callback_query(ProjectOptionClass.filter(F.btn_purpose == "free_subscription"))
async def free_subscription(query:types.CallbackQuery , callback_data , state:FSMContext)->None:
    await state.clear()
    await query.message.answer(text = Succeed_Free_Signals)
    await query.answer()




    

