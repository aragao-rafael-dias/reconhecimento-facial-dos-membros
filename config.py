import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("MYSQL_ROOT_PASSWORD")
    DB_HOST = os.getenv("MYSQL_HOST")
    DB_USER= os.getenv("MYSQL_USER")
    DB_PASSWORD =  os.getenv("MYSQL_PASSWORD")
    DB_NAME =  os.getenv("MYSQL_DATABASE")

print(f"DB_HOST: {os.getenv('MYSQL_HOST')}")

