from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from Keyboards.keyboard_classes import SignalClass


async def invite_link_keyboard(invite_link):
    button1 = InlineKeyboardButton(text="Click To Join!" , url=invite_link )

    builder = InlineKeyboardBuilder([[button1]])
    builder.adjust(1)
    keyboard = builder.as_markup()
    return keyboard

async def free_invite_link_keyboard(invite_link):
    button1 = InlineKeyboardButton(text="Click To Join!" , url=invite_link )

    builder = InlineKeyboardBuilder([[button1]])
    builder.adjust(1)
    keyboard = builder.as_markup()
    return keyboard