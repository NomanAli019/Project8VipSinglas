from Keyboards.keyboard_classes import PromocodeClass
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

async def promo_code_option():
    button1 = InlineKeyboardButton(text="Yes"  ,  callback_data=PromocodeClass(btn_type="yes" ).pack())
    button2 = InlineKeyboardButton(text="No" , callback_data=PromocodeClass(btn_type="no").pack())
    builder = InlineKeyboardBuilder([[button1, button2]])
    builder.adjust(2)
    keyboard = builder.as_markup()
    return keyboard