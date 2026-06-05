
# File: Centralized Environment Configuration & Validation
# (Yeh file pure application ke configurations aur secret credentials 
# ko ek jagah manage karti hai taaki code pure environment me securely run ho sake.)

import os   #Python ke built-in 'os' (Operating System) module ko import karta hai system environment variables access karne ke liye.
from dotenv import load_dotenv  #python-dotenv' library se load_dotenv function lata hai taaki project directory se '.env' file read ho sake.
import logging  #Application logging setup karne ke liye standard library logging module import karta hai (print() statements production me allow nahi hote).

from app.common.error import InternalError # Is project ka custom exception handler 'InternalError' import kiya ja raha hai structural standard framework maintain karne ke liye.

load_dotenv()


class Config:
    version = "0.1.0"
    title = "releads"

    app_settings = {
        'db_name': os.getenv('MONGO_DB'),
        'mongodb_url': os.getenv('MONGO_URL'),
        'db_username': os.getenv('MONGO_USER'),
        'db_password': os.getenv('MONGO_PASSWORD'),
        'max_db_conn_count': os.getenv('MAX_CONNECTIONS_COUNT'),
        'min_db_conn_count': os.getenv('MIN_CONNECTIONS_COUNT'),
    }

    @classmethod
    def app_settings_validate(cls):
        for k, v in cls.app_settings.items():
            if None is v:
                logging.error(f'Config variable error. {k} cannot be None')
                raise InternalError([{"message": "Server configure error"}])
            else:
                logging.info(f'Config variable {k} is {v}')



