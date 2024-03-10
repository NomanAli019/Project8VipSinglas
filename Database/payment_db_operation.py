import asyncio
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from Database.models import engine , Base , session , Payment
from sqlalchemy import func

async def check_payment(id):
    payment = session.query(Payment).filter_by(user_id=id).first()
    if payment:
        return payment
    else:
        return None

async def update_payment(user_id , status):
    payment_stat = session.query(Payment).filter_by(user_id=user_id).first()
    if payment_stat:
        payment_stat.payment_status = status 
        session.commit()

async def add_payment(user_id  , user_name  , status):
    payment_addition = Payment(user_id=user_id , user_name=user_name , payment_status = status)
    session.add(payment_addition)
    session.commit()
    if payment_addition:
        return True
    else:
        return False
    
async def delete_payment(user_id):
    user_payment = session.query(Payment).filter_by(user_id=user_id).first()
    if user_payment:
        session.delete(user_payment)
        session.commit()