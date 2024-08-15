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

def create_user(userName, password, newUserName, newPassword):
    engine = create_engine(f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}")
    Session = sessionmaker(bind=engine)  

    session = Session()

    # Verify existing user
    existing_user = session.query(User).filter_by(username=userName, password=password).first()
    userId= existing_user.userid
    if not existing_user:
        # Handle invalid credentials
        return False

    # Create new user
    new_user = User(username=newUserName, password=newPassword)
    session.add(new_user)
    session.commit()
    session.close()
    return userId

def authenticate_user(userName, password):
    engine = create_engine(f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}")
    Session = sessionmaker(bind=engine)  

    session = Session()
    existing_user = session.query(User).filter_by(username=userName, password=password).first()
    userId= existing_user.userid
    if not existing_user:
        # Handle invalid credentials
        return False
    else:
        return userId
def create_log(userId, requestType, content, response):
    engine = create_engine(f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}")
    Session = sessionmaker(bind=engine)  

    session = Session()
    new_log = Log(
        userid=userId,
        date=datetime.datetime.now(),
        requesttype=requestType,
        content=json.dumps(content),
        response=json.dumps(response)
    )
    session.add(new_log)
    session.commit()
    session.close()