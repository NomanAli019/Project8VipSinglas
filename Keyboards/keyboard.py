from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from Keyboards.keyboard_classes import StartClass , ProjectOptionClass

async def start_keyboard():
    button1 = InlineKeyboardButton(text="Start" , callback_data=StartClass(btn_type="start",btn_name="start_button").pack())

    builder = InlineKeyboardBuilder([[button1]])
    builder.adjust(1)
    keyboard = builder.as_markup()
    return keyboard

async def project_option_keyboard():
    button1 = InlineKeyboardButton(text="Project 8 VIP Subscription" , callback_data=ProjectOptionClass(btn_type="subs" , btn_purpose="vip_subscription").pack())
    button2 = InlineKeyboardButton(text="Project 8 FREE Model" , callback_data=ProjectOptionClass(btn_type="subs",btn_purpose="free_subscription").pack())
    builder = InlineKeyboardBuilder([[button1 , button2]])
    builder.adjust(2)
    keyboard = builder.as_markup()
    return keyboard



