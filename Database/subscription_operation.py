import asyncio
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from Database.models import engine , Base , session , Subscription
from sqlalchemy import func

async def check_user_subscription(user_id):
    subscription = session.query(Subscription).filter_by(user_id=user_id).first()
    if subscription:
        return True
    else:
        return False
    
async def add_subscription(user_id , subscription_time , subscription_type):
    adding_subs = Subscription(user_id=user_id , subs_time = subscription_time , subs_type=subscription_type)
    session.add(adding_subs)
    session.commit()
    if adding_subs:
        return True
    else:
        return False
    
async def get_user_subscription_data(user_id):
    try:
        subscription_data = session.query(Subscription).filter_by(user_id = user_id).first()
        if subscription_data:
            return subscription_data
        else:
            return False
    except Exception as e:
        return False

async def get_all_subscriber():
    try:
        subs = session.query(Subscription).all()
        return subs
    except Exception as e:
        return None

async def delete_subscription(user_id):
    user_sub = session.query(Subscription).filter_by(user_id=user_id).first()
    if user_sub:
        session.delete(user_sub)
        session.commit()

async def update_subscription(user_id , new_date_time):
    user_subs = session.query(Subscription).filter_by(user_id=user_id).first()
    if user_subs:
        user_subs.subs_time = new_date_time 
        session.commit()