# configurations ka use karke application database se kaise connect hota 
# hai aur connection pool kaise banta hai.

import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
#  AsyncIOMotorClient: Yeh aapki application aur MongoDB server ke beech ka Main Bridge (Client) hai.
#  AsyncIOMotorDatabase: Yeh pure MongoDB server ke andar se kisi ek specific database ko represent karta hai.
import logging

from app.conf.config import Config

load_dotenv()

db_client: AsyncIOMotorClient = None 
# db_client = None (The Logic):

    # 1. Jab application start hoti hai, tab turant database connect nahi hota. Isliye shuruat mein hum is variable ko empty
    #(None) rakh dete hain.

    # 2. Jab baad mein connect_and_init_db() function chalta hai, tab is None ki jagah asli active connection object 
    #(AsyncIOMotorClient) baith jata hai.

    # 3. AsyncIOMotorClient: Type hint : Yeh Python ko (aur aapke Code Editor/VS Code ko) bata raha hai ki "Bhai, is 
    # db_client variable ke andar aage chal kar jo data aayega, woh AsyncIOMotorClient ka object hi hoga."


async def get_db() -> AsyncIOMotorDatabase:       # Works as database provider
    db_name = Config.app_settings.get('db_name')
    return db_client[db_name]   # db_client ke aage [] lagakar kisi database ka naam likhte hain, toh Python    
                                # samajh jata hai ki "Pure server mein se mujhe is specific database ke andar jana hai.
# db_client ke paas in sabhi databases ka access hota hai


# Iska kaam hai Application aur MongoDB ke beech ka rasta (Connection) banana aur use shuru karna.
# Jab aapki web application (jaise FastAPI) start hoti hai, toh sabse pehle isi function ko call kiya jata hai taaki 
# database se dosti pakki ho sake.
async def connect_and_init_db():

    global db_client

    # Iska kya matlab hai? Humne file ke shuruat mein db_client = None banaya tha. Is function ke andar global keyword 
    # ka use karne ka matlab hai: "Mai isi file ke bahar wale db_client variable ko badalne ja raha hoon.
    
    try:
        # AsyncIOMotorClient ko call karte hi MongoDB server se connection jodne ki prakriya shuru ho jati hai.
        # Hum iske andar saari settings pass kar rahe hain
        db_client = AsyncIOMotorClient(
            Config.app_settings.get('mongodb_url'),
            username=Config.app_settings.get('db_username'),
            password=Config.app_settings.get('db_password'),
            maxPoolSize=Config.app_settings.get('max_db_conn_count'),
            minPoolSize=Config.app_settings.get('min_db_conn_count'),
            uuidRepresentation="standard",  # Agar aap data mein UUID (Unique IDs) use karte hain, toh yeh use Python 
                                            # aur MongoDB ke bich standard format mein convert karta hai (varna binary 
                                            # data mein dikkat aati hai).
        )
        logging.info('Connected to mongo.')
    except Exception as e:
        logging.exception(f'Could not connect to mongo: {e}')
        raise   # Yeh error ko aage bhej dega (re-throw karega), jiska matlab hai: "Agar database hi connect nahi hua, 
                # toh application ko aage mat badhao, yahin rok do!" Kyunki bina database ke app chalne ka koi faayda nahi hai.


async def close_db_connect():
    global db_client
    if db_client is None:
        logging.warning('Connection is None, nothing to close.')
        return
    db_client.close()
    db_client = None
    logging.info('Mongo connection closed.')

# End of file
