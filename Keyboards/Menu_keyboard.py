from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from Keyboards.keyboard_classes import MenuClass

async def subs_menu_keyboard():
    button1 = InlineKeyboardButton(text="Menu" , callback_data=MenuClass(btn_type="Menu" , btn_purpose="subscription_menu").pack())
    button2 = InlineKeyboardButton(text="Cancel Subscription ❌" , callback_data=MenuClass(btn_type="cancel_subs" , btn_purpose="cancel_subscription").pack())
    button3 = InlineKeyboardButton(text="Renew Subscription 🆕" , callback_data=MenuClass(btn_type="Renew_subs" , btn_purpose="Renew_subscription").pack())
    button4 = InlineKeyboardButton(text="Refresh 🔃" , callback_data=MenuClass(btn_type="Refres_view" , btn_purpose="Refreshing_view").pack())

    builder = InlineKeyboardBuilder([[button1 , button2 , button3 , button4]])
    builder.adjust(1,2,1)
    keyboard = builder.as_markup()
    return keyboard