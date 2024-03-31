from Keyboards.keyboard_classes import CancelSubscribeClass
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

async def cancel_sub_option():
    button1 = InlineKeyboardButton(text="Yes"  ,  callback_data=CancelSubscribeClass(btn_type="yes" ).pack())
    button2 = InlineKeyboardButton(text="No" , callback_data=CancelSubscribeClass(btn_type="no").pack())
    builder = InlineKeyboardBuilder([[button1, button2]])
    builder.adjust(2)
    keyboard = builder.as_markup()
    return keyboard