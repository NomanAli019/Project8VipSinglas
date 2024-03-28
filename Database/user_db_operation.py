import asyncio
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from Database.models import engine , Base , session , User
from sqlalchemy import func 

async def get_users():
    users = session.query(User).all()
    return users
    
async def check_user(user_id):
    try:
        user = session.query(User).filter_by(chat_id=user_id).first()
        if user:
            return True
        else:
            return False
    except Exception as e:
        return False    
    
async def add_user(user_id, pocket_account_id ,user_name , promo_code):
    new_user = User(chat_id=user_id , pocket_option_account_id=pocket_account_id , user_name=user_name , promo_code=promo_code)
    session.add(new_user)
    session.commit()