import asyncio
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from Database.models import engine , Base , session , UserPromoCodeUse
from sqlalchemy import func


async def add_user_promo_code_status(user_id, status):
    promo_code_addition = UserPromoCodeUse(user_id=user_id , promo_code_status=status)
    print(promo_code_addition)
    session.add(promo_code_addition)
    session.commit()
   
    
async def get_promo_code(user_id):
    try:
        user_promo_code_data = session.query(UserPromoCodeUse).filter_by(user_id=user_id).first()
        if user_promo_code_data:
            return user_promo_code_data
        else:
            return None
    except Exception as e:
        return None

async def update_promo_code(user_id , status):
    promo_code_data = session.query(UserPromoCodeUse).filter_by(user_id=user_id).first()
    if promo_code_data:
        promo_code_data.promo_code_status = status 
        session.commit()