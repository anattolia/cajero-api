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

def create_user(new_user_in_db: UserInDB):
    database_users[new_user_in_db.username]= new_user_in_db
    return new_user_in_db

def get_all_users():
    return database_users.values()        

