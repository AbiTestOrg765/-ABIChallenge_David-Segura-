from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json
import datetime
Base = declarative_base()

db_config = {
    'database': 'appMl',
    'user': 'david',
    'password': 'david123',
    'host': 'localhost',
    'port': '5432'
}


class User(Base):
    __tablename__ = 'users'
    userid = Column(Integer, primary_key=True)

    username = Column(String)
    password = Column(String)

class Log(Base):
    __tablename__ = 'logs'
    logid = Column(Integer, primary_key=True)
    userid = Column(Integer, ForeignKey('users.userid'))
    date = Column(DateTime)
    requesttype= Column(String)
    content = Column(String)
    response = Column(String)

def create_user(user_name, password, new_user_name, new_password):
    engine = create_engine(f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}")
    session = sessionmaker(bind=engine)  

    session_user = session()

    # Verify existing user
    existing_user = session_user.query(User).filter_by(username=user_name, password=password).first()
    user_id= existing_user.userid
    if not existing_user:
        # Handle invalid credentials
        return False

    # Create new user
    new_user = User(username=new_user_name, password=new_password)
    session_user.add(new_user)
    session_user.commit()
    session_user.close()
    return user_id

def authenticate_user(user_name, password):
    engine = create_engine(f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}")
    session = sessionmaker(bind=engine)  

    session_user = session()
    existing_user = session_user.query(User).filter_by(username=user_name, password=password).first()
    user_id= existing_user.userid
    if not existing_user:
        # Handle invalid credentials
        return False
    else:
        return user_id

def create_log(user_id, request_type, content, response):
    engine = create_engine(f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}")
    session = sessionmaker(bind=engine)  

    session_log = session()
    new_log = Log(
        userid=user_id,
        date=datetime.datetime.now(),
        requesttype=request_type,
        content=json.dumps(content),
        response=json.dumps(response)
    )
    session_log.add(new_log)
    session_log.commit()
    session_log.close()