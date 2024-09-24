import os

class Config:
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_NAME = os.getenv('DB_NAME')
    SECRET_KEY1 = os.getenv('STORMGLASS_API_KEY')
    SECRET_KEY2 = os.getenv('STORMGLASS_API_KEY2')
