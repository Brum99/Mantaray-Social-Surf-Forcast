from flask_login import UserMixin
from database import get_db_connection

class User(UserMixin):
    def __init__(self, user_id, username, email, password):
        self.id = user_id
        self.username = username
        self.email = email
        self.password = password

    @staticmethod
    def get(user_id):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT user_id, username, email, password FROM users WHERE user_id = %s", (user_id,))
        user_data = cursor.fetchone()
        cursor.close()
        connection.close()

        if user_data:
            return User(*user_data)
        return None

    @staticmethod
    def find_by_username(username):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT user_id, username, email, password FROM users WHERE username = %s", (username,))
        user_data = cursor.fetchone()
        cursor.close()
        connection.close()

        if user_data:
            return User(*user_data)
        return None