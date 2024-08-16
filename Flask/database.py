from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json
import datetime
import os
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    user_name = Column(String)
    password = Column(String)

class Log(Base):
    __tablename__ = 'logs'
    log_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.userid'))
    date = Column(DateTime)
    end_point = Column(String)
    request_type= Column(String)
    content = Column(String)
    response = Column(String)

class Database:
    def __init__(self):
        # Load Database credentials
        db_config = {
            'database': os.environ.get('DB_NAME'),
            'user': os.environ.get('DB_USER'),
            'password': os.environ.get('DB_PASSWORD'),
            'host': os.environ.get('DB_HOST'),
            'port': os.environ.get('DB_PORT')  
        }

        #Connect to postgres DB
        self.engine = create_engine(f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}")
        session = sessionmaker(bind=self.engine)  

        self.session = session()

    def create_user(self, user_name, password, new_user_name, new_password):
        """ Function used to create new users
        Args:
            user_name (string): Name of an existing account
            password (string): Password for an existing account
            new_user_name (string): New name of a new account
            new_password (string): New password for an new account
        Returns:
            user_id (array): The Id of the user that created the new account
        
        """
        # Verify existing user
        existing_user = self.session.query(User).filter_by(username=user_name, password=password).first()
        user_id= existing_user.userid
        if not existing_user:
            # Handle invalid credentials
            return False

        # Create new user
        new_user = User(username=new_user_name, password=new_password)
        self.session.add(new_user)
        self.session.commit()
        self.session.close()
        return user_id

    def authenticate_user(self, user_name, password):
        """ Function used to verify the credentials of users
        Args:
            user_name (string): Name of an existing account
            password (string): Password for an existing account
        Returns:
            user_id (array): The Id of the user that created the new account
        
        """
        existing_user = self.session.query(User).filter_by(username=user_name, password=password).first()
        user_id= existing_user.userid
        if not existing_user:
            # Handle invalid credentials
            return False
        else:
            #Return user id
            return user_id

    def create_log(self, user_id, end_point, request_type, content, response):
        """ Function used to create logs on the db
        Args:
            user_id (string): Name of an existing account
            end_point (string): endpoint that is calling this function
            request_type (string): Type of request
            content (string): the body of the request
            response (string): The response for that request
        
        """
        # Creates new log object
        new_log = Log(
            userid=user_id,
            date=datetime.datetime.now(),
            requesttype=request_type,
            end_point = end_point,
            content=json.dumps(content),
            response=json.dumps(response)
        )
        # Adds log to db
        self.session.add(new_log)
        self.session.commit()
        self.session.close()