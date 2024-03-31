import asyncio
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from Database.models import engine , Base , session , UserReminder
from sqlalchemy import func 

async def add_reminder(user_id  , reminder):
    reminder_addition = UserReminder(user_id=user_id  , remainder_status=reminder)
    session.add(reminder_addition)
    session.commit()

async def check_reminder(user_id):
    try:
        reminder = session.query(UserReminder).filter_by(user_id=user_id).first()
        if reminder:
            return reminder
        else:
            return None
    except Exception as e:
        return None
        

async def delete_reminder(user_id):
    user_reminder = session.query(UserReminder).filter_by(user_id=user_id).first()
    if user_reminder:
        session.delete(user_reminder)
        session.commit()
    
