
# File: Centralized Environment Configuration & Validation
# (Yeh file pure application ke configurations aur secret credentials 
# ko ek jagah manage karti hai taaki code pure environment me securely run ho sake.)

import os   #Python ke built-in 'os' (Operating System) module ko import karta hai system environment variables access karne ke liye.
from dotenv import load_dotenv  #python-dotenv' library se load_dotenv function lata hai taaki project directory se '.env' file read ho sake.
import logging  # Application logging setup karne ke liye standard library logging module import karta hai (print() statements production me allow nahi hote).

from app.common.error import InternalError # Is project ka custom exception handler 'InternalError' import kiya ja raha hai structural standard framework maintain karne ke liye.

load_dotenv()   # load_dotenv() :Laptop par .env file ke passwords ko uthakar Python ki temporary memory (RAM) me daalta hai.
                # os.getenv(): Python ki usi memory se password ko read karke code ke andar use karta hai.

class Config:   #Configuration namespace define karne ke liye ek standard Class block banaya gaya hai.
    version = "0.1.0" # Yeh aapki API ya aapke project ka naam (Name) hai.
    title = "releads" # Yeh aapke app ka kaun sa number ka model (Version Number) chal raha hai, wo batata hai.

    app_settings = { # Ek configuration Dictionary data structure jo memory se sensitive details load karti hai.
        'db_name': os.getenv('MONGO_DB'),
        'mongodb_url': os.getenv('MONGO_URL'),
        'db_username': os.getenv('MONGO_USER'),
        'db_password': os.getenv('MONGO_PASSWORD'),
        'max_db_conn_count': os.getenv('MAX_CONNECTIONS_COUNT'),    # Connection-pool-settings
        'min_db_conn_count': os.getenv('MIN_CONNECTIONS_COUNT'),    # Connection-pool-settings
    }

    @classmethod # yeh FastAPI ka part nahi hai, yeh core Python ka ek built-in feature (decorator) hai.

    # 1. Normal Python classes mein jab aap koi method banate hain, toh use chalane ke liye pehle class ka 
    # ek object/instance banana padta hai
    
    # 2.Lekin @classmethod lagane ke baad, aapko koi object banane ki zaroorat nahi padti. Aap direct Class ke
    # naam se hi us method ko call kar sakte hain

    def app_settings_validate(cls): # Method declaration jo explicit application validation boot trigger setup karta hai.
        
        for k, v in cls.app_settings.items():   # Dictionary key-value elements par loop running strategy taaki automated dynamically monitoring ho sake.
            
            if None is v:   # Critical Sanity Check. Agar system variable read nahi ho paya toh wo 'None' default value return karta hai.
                
                logging.error(f'Config variable error. {k} cannot be None') 
                # Server terminal output par application level high-severity error message emit karta hai telemetry alerts ke liye.
                
                raise InternalError([{"message": "Server configure error"}])
                # Fail-Fast principle implementing block: Custom runtime failure exception throw karke system booting execution ko halt kar deta hai.
            else:
                logging.info(f'Config variable {k} is {v}')
                #Operational logs capture metadata configuration confirmation tracking ke liye.


            ## What is use of this for loop
            
            # 1. Terminal Par Track Karna (logging.info): Jab saare variables .env file se sahi-sahi load ho jate hain,
            # toh yeh loop terminal par print karta hai ki kaun se variable me kya value aayi hai (jaise kis database ya 
            # URL se connection ban raha hai). Isse developer ko validation ka live proof/tracking mil jata hai.
            
            # 2. Server Crashing Alert (logging.error + raise): Agar koi zaroori variable (jaise database password)
            #  missing hai, toh yeh sirf terminal par error nahi dikhata, balki server ko chalne se hi rok deta hai 
            # (crash kar deta hai). 

            ## Very Important : 
            # Fail-Fast Principle: "The configuration validator implements the 'Fail-Fast' architecture principle. 
            # Instead of letting the application boot with bad or missing configurations—which would cause 
            # silent runtime failures later when users try to read/write data—we trigger a validation loop at startup. 
            # If a dependency is missing, we immediately halt execution, log a high-severity error to the telemetry, 
            # and crash the process safely before it accepts traffic."



#----------------------------------------------------------------------------------------------------------------------

## IMP : Difference btw .env file and Environment Variables

# .env file: Laptop Par (Local): Tum baar-baar Operating System ki settings me jaakar variables manually set nahi 
# karna chahte, isliye tum ek .env file bana dete ho. python-dotenv library is file se values 
# utha kar tumhare local code ko de deti hai.

# environment Variables: Server Par (Production): Wahan koi .env file nahi hoti. Wahan variables direct Linux OS ya 
# Docker container settings me save hote hain. Jab server par application chalta hai, 
# toh wo direct OS se unhe read kar leta hai.

# Adv: Isse tumhara code safe rehta hai aur bina badle dono jagah chal jata hai. Great catch!

#--------------------------------------------------------------------------------------------------------------------
## version and title

# title: Jab aapka FastAPI app run hota hai aur aap uske documentation page par jaate ho (http://localhost:8000/docs),
# toh sabse upar bade-bade aksharon mein jo naam dikhta hai, yeh wahi hai. Isse users ko pata chalta hai ki yeh kis 
# cheez ki API hai.

#version: Jab aap pehli baar app banate ho, toh aap use 0.1.0 bolte ho. Baad mein jab aap naye features add karoge ya 
# bugs fix karoge, toh aap is number ko badha kar 0.2.0 ya 1.0.0 kar doge. Isse developers aur users ko pata chalta hai 
# ki unke paas bilkul latest code chal raha hai ya purana.

#--------------------------------------------------------------------------------------------------------------------

# # IMP : What is Database Connection Pooling? ** VERY IMPORTANT

# Connection pooling is a cache of database connections maintained by the driver so that connections can be reused when 
# future requests to the database are required. Instead of executing an expensive TCP handshake to open and close a 
# socket for every single query, connections are kept alive in a pool, significantly reducing operational latency and 
# improving application throughput.