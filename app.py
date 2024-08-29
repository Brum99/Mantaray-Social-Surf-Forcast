from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
import os
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Used for session management

def get_db_connection():
    connection = mysql.connector.connect(
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host='localhost',
        database=os.getenv('DB_NAME')
    )
    return connection

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)  # No method specified
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
                       (username, email, hashed_password))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Account created successfully. You can now log in.')
        return redirect(url_for('login'))
    
    return render_template('sign_up.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if result and check_password_hash(result[0], password):
            session['user'] = username
            flash('Logged in successfully.')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials. Please try again.')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.')
    return redirect(url_for('login'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/map')
def map_page():
    return render_template('map.html')

if __name__ == '__main__':
    app.run(debug=True)
