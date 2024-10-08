from aiogram.filters.callback_data import CallbackData

class StartClass(CallbackData,prefix="Sbtn"):
    btn_type:str
    btn_name:str


class ProjectOptionClass(CallbackData, prefix="btn"):
    btn_type:str
    btn_purpose:str

class SignalClass(CallbackData, prefix="btn"):
    btn_type:str
    btn_purpose:str

class MenuClass(CallbackData , prefix="btn"):
    btn_type:str
    btn_purpose:str

class SubscriberClass(CallbackData, prefix="btn"):
    btn_type:str

class CancelSubscribeClass(CallbackData, prefix="btn"):
    btn_type:str

class PromocodeClass(CallbackData , prefix="btn"):
    btn_type:str