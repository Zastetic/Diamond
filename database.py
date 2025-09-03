from sqlalchemy import create_engine, String, Integer, Column #type ignore
from sqlalchemy.orm import sessionmaker, declarative_base #type: ignore
from sqlalchemy.inspection import inspect #type: ignore

db = create_engine("sqlite:///database/clients")
Session = sessionmaker(bind=db)
session = Session()

Base = declarative_base()

# DECLARING TABLE
class User(Base):
    __tablename__="User"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column("username", String)
    email = Column("email", String, unique=True)
    password = Column("password", String)

    def __init__(self, email, password, username):
        self.email = email
        self.password = password
        self.username = username
    
    def __repr__(self, email, password, username):
        return f"Email: {email}, Password: {password}, user: {username}"

# data = [
#     User(email="vh555@gmail.com", password="12345678")
# ]
# session.add_all(data)
# session.commit()
Base.metadata.create_all(bind=db)
