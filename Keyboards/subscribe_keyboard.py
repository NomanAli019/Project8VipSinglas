from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from Keyboards.keyboard_classes import SubscriberClass

async def subscriber_button(transaction_url):

    button1 = InlineKeyboardButton(text="Click To Subscribe!" , url=transaction_url , callback_data=SubscriberClass(btn_type="subscribe").pack())
    builder = InlineKeyboardBuilder([[button1]])
    builder.adjust(1)
    keyboard = builder.as_markup()
    return keyboard

