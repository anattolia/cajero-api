from typing import Dict
from pydantic import BaseModel

class UserInDB(BaseModel): #UserInDb extiende de BaseModel -> herencia en python
    username: str
    password: str
    balance: int

database_users = Dict[str, UserInDB]
database_users = {
    "camilo24": UserInDB(**{"username":"camilo24",
                            "password": "root",
                            "balance":12000}),
    
    "andres18": UserInDB(**{"username":"andres18",
                            "password":"hola",
                            "balance":34000}),
}

def get_user(username: str):
    if username in database_users.keys():
        return database_users[username]
    else:
        return None

def update_user(user_in_db: UserInDB):
    database_users[user_in_db.username] = user_in_db
    return user_in_db

database_users_list = []
generator = {"username":"Juan",
              "password":"hola2",
              
              }

def create_user(user_in_db: UserInDB):
    generator["username", "password"] = generator
    user_in_db.username = generator["username"]
    user_in_db.password = generator["password"]
  
    database_users_list.append(user_in_db)
    return user_in_db


