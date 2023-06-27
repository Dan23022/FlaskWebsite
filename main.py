import sqlite3

import bcrypt as bcrypt
from flask import *

app = Flask(__name__)

@app.route('/')
def login_page():
    return render_template('login_page.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['email']
    password = request.form['password'].encode('utf-8')

    connect = sqlite3.connect("misc/main_db")
    cur = connect.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS logins (username TEXT, password TEXT)")
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
    cur.execute("INSERT INTO logins (username, password) VALUES (?, ?)", (username, hashed_password))
    connect.commit()

    return "Registration Successful"

@app.route('/login', methods=['POST'])
def login():

    username = request.form['email']
    password = request.form['password'].encode('utf-8')

    connect = sqlite3.connect("misc/main_db")
    cur = connect.cursor()
    cur.execute("SELECT password FROM logins WHERE username = ?", (username,))
    result = cur.fetchone()

    if result and bcrypt.checkpw(password, result[0]):
        cur.close()
        return "Login Successful"
    else:
        return "Login Failed"


if __name__ == '__main__':
    app.run(debug=True)
