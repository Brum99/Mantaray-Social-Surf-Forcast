import mysql.connector
from config import Config

def get_db_connection():
    connection = mysql.connector.connect(
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        host='localhost',
        database=Config.DB_NAME
    )
    return connection

def query_all_users():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    connection.close()
    return users
