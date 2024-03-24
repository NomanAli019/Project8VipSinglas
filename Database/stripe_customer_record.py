import asyncio
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from Database.models import engine , Base , session , StripeCustomerRecord
from sqlalchemy import func 

async def check_stripe_customer(user_id):
    customer_record = session.query(StripeCustomerRecord).filter_by(user_id=user_id).first()
    if customer_record:
        return True
    else:
        return False
    
async def get_customer_record(user_id):
    customer_rec = session.query(StripeCustomerRecord).filter_by(user_id=user_id).first()
    return customer_rec
    
async def add_stripe_customer(user_id , customer_id):
    adding_stripe = StripeCustomerRecord(user_id=user_id , stripe_cus_id=customer_id)
    session.add(adding_stripe)
    session.commit()
    
    
async def delete_customer(user_id):
    stripe_cus_data = session.query(StripeCustomerRecord).filter_by(user_id=user_id).first()
    if stripe_cus_data:
        session.delete(stripe_cus_data)
        session.commit()