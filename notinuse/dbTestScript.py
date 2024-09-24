import mysql.connector
import os 

def test_db_connection():
    # Print environment variables to verify they are loaded
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_name = os.getenv('DB_NAME')
    
    print(f"DB_USER: {db_user}")
    print(f"DB_PASSWORD: {db_password}")
    print(f"DB_NAME: {db_name}")

    try:
        # Configure the connection
        cnx = mysql.connector.connect(
            user=db_user,
            password=db_password,
            host='localhost',
            database=db_name
        )
        
        cursor = cnx.cursor()
        cursor.execute("SELECT DATABASE()")  # Query to check the database connection
        result = cursor.fetchone()
        
        if result:
            print(f"Connected to database: {result[0]}")
        else:
            print("Failed to connect to the database")
        
        cursor.close()
        cnx.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

if __name__ == '__main__':
    test_db_connection()



