import asyncio
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from Database.models import engine , Base , session , User
from sqlalchemy import func 

async def get_users():
    users = session.query(User).all()
    return users
    
async def get_user_data(user_id):
    try:
        user = session.query(User).filter_by(chat_id=user_id).first()
        if user:
            return user
        else:
            return None
    except Exception as e:
        return None


async def check_user(user_id):
    try:
        user = session.query(User).filter_by(chat_id=user_id).first()
        if user:
            return True
        else:
            return False
    except Exception as e:
        return False    

async def update_user_promo_code_status(user_id , p_code_status):
    user = session.query(User).filter_by(chat_id=user_id).first()
    if user:
        user.promo_code_status = p_code_status
        session.commit()

async def update_user_customer_id(user_id , customer_id):
    user = session.query(User).filter_by(chat_id=user_id).first()
    if user:
        user.strip_customer_id = customer_id
        session.commit()
    

async def update_user_sub_status(user_id , sub_status):
    user = session.query(User).filter_by(chat_id=user_id).first()
    if user:
        user.subscription_status = sub_status
        session.commit()

async def add_user(user_id, pocket_account_id ,user_name , promo_code , p_code_status , s_cus_id , sub_status):
    new_user = User(chat_id=user_id , pocket_option_account_id=pocket_account_id , user_name=user_name , promo_code=promo_code ,promo_code_status=p_code_status , strip_customer_id=s_cus_id , subscription_status=sub_status)
    session.add(new_user)
    session.commit()