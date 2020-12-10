from db.user_db import UserInDB
from db.user_db import update_user, get_user, create_user, get_all_users
from db.transaction_db import TransacionInDb
from db.transaction_db import save_transaction
from models.user_models import UserIn, UserOut, UserInCreate
from models.transaction_models import TransactionIn, TransactionOut

import datetime
from fastapi import FastAPI
from fastapi import HTTPException 

api = FastAPI()

#####
from fastapi.middleware.cors import CORSMiddleware
origins = [
"http://localhost.tiangolo.com", 
"https://localhost.tiangolo.com",
"http://localhost", 
"http://localhost:8080", 
"https://cajero-app-antonia.herokuapp.com",
]
api.add_middleware(
CORSMiddleware, allow_origins=origins,
allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

#Para asociar esta función a un navegador web: @api.xxx -> "post" puede ser "get", "put" o cualquier otro método HTTP
#la URL es de la petición
@api.post("/user/auth/")
#async permite ejecutar distintos procesos independientemente, sin tener que esperar a que terminen todos los demás procesos
#Se usa en las definiciones de las peticiones
async def auth_user(user_in: UserIn):
    #Verifica si el usuario existe en la base de datos y retorna su info, si existe
    user_in_db = get_user(user_in.username)
    #Si el usuario no está en la base de datos, devuelve una excepción HTTP y un mensaje de error
    if user_in_db == None:
       raise HTTPException(status_code=404, detail="El usuario no existe")
    #Comprueba si el password ingresado es diferente o no a la almacenada en la base de datos
    if user_in_db.password != user_in.password:
       return {"Autenticado": False}
    return {"Autenticado": True}


@api.get("/user/balance/{username}")
async def get_balance(username: str):
    user_in_db = get_user(username)
    if user_in_db == None:
        raise HTTPException(status_code=404, detail="El usuario no existe")
    #El ** mapea y devuelve, de todos los campos del diccionario, solo los que existen en el objeto de salida (UserOut en este caso)
    user_out = UserOut(**user_in_db.dict())
    return user_out

@api.put("/user/transaction/")
async def make_transaction(transaction_in: TransactionIn):

    user_in_db = get_user(transaction_in.username)

    if user_in_db == None:
        raise HTTPException(status_code=404, detail="El usuario no existe")

    if user_in_db.balance < transaction_in.value:
        raise HTTPException(status_code=400, detail="Fondos insuficientes")

    user_in_db.balance = user_in_db.balance - transaction_in.value
    update_user(user_in_db)

    transaction_in_db = TransacionInDb(**transaction_in.dict(),
                                            actual_balance = user_in_db.balance)
    transaction_in_db = save_transaction(transaction_in_db)

    transaction_out = TransactionOut(**transaction_in_db.dict())
    return transaction_out


@api.put("/user/create/")
async def user_create(user_in: UserIn):
    user_in_db = get_user(user_in.username)
    if user_in_db == None:
        user_in_db = create_user(user_in)
        
    user_out = UserIn(**user_in_db.dict())
   # return user_out.username
    return {"Creado": True}

@api.get("/user/list")
async def list_users():
    users_in_db=get_all_users()
    users_out=[]
    for user in users_in_db:
        user_out = UserOut(**user.dict())
        users_out.append(user_out)
    return users_out 