from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date,BigInteger , DATETIME
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer, nullable=False)
    pocket_option_account_id = Column(Integer , nullable=False)
    user_name = Column(String(50), nullable=False)

class Subscription(Base):
    __tablename__ = "Subscriptions"
    id = Column(Integer , primary_key=True , autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subs_time = Column(DATETIME , nullable=False)
    subs_type = Column(String(50) , nullable=False)

class Payment(Base):
    __tablename__ = "Payments"
    id = Column(Integer , primary_key=True , autoincrement=True)
    user_id = Column(Integer , ForeignKey("users.id") ,nullable=False)
    user_name = Column(String(50) , nullable=False)
    payment_status = Column(String(50) , nullable=False)

class UserRemainder(Base):
    __tablename__= "userremainder"
    id = Column(Integer , primary_key=True , autoincrement=True)
    user_id  = Column(Integer , ForeignKey("users.id") ,nullable=False)
    remainder_status = Column(String(50) , nullable=False)

# class UserCardData(Base):
#     id = Column(Integer , primary_key=True , autoincrement=True)
#     user_id  = Column(Integer , ForeignKey("users.id") ,nullable=False)
#     email 
#     card_number 
#     cvv
#     expiry
#     zip_code 
#     card_holder_name
#     region

engine = create_engine('sqlite:///project8db.db')  
Session = sessionmaker(bind=engine)
session = Session()

# Base.metadata.create_all(engine)