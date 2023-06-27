import os
import sqlite3
import bcrypt
from flask import Flask, render_template, request, redirect, jsonify, session
from flask.views import MethodView

class ChatApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'your-secret-key'
        self.setup_database()

    def setup_database(self):
        conn = sqlite3.connect("misc/chat.db")
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, message TEXT)")
        conn.commit()
        conn.close()

    def setup_routes(self):
        self.app.add_url_rule('/', view_func=LoginPage.as_view('login_page'))
        self.app.add_url_rule('/register', view_func=LoginPage.as_view('register'))
        self.app.add_url_rule('/login', view_func=Login.as_view('login'))
        self.app.add_url_rule('/chatroom', view_func=ChatRoom.as_view('chatroom'))
        self.app.add_url_rule('/send_message', view_func=SendMessage.as_view('send_message'))
        self.app.add_url_rule('/get_messages', view_func=GetMessages.as_view('get_messages'))

    def run(self, host='localhost', port=5000):
        self.setup_routes()
        self.app.run(host=host, port=port, debug=True)

class ChatRoom(MethodView):
    def get(self):
        username = session.get('username')
        return render_template('chatroom.html', username=username)

class LoginPage(MethodView):
    def get(self):
        return render_template('login_page.html')

    def post(self):
        username = request.form['email']
        password = request.form['password'].encode('utf-8')

        connect = sqlite3.connect("misc/main_db")
        cur = connect.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS logins (username TEXT, password TEXT)")
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
        cur.execute("INSERT INTO logins (username, password) VALUES (?, ?)", (username, hashed_password))
        connect.commit()

        return redirect('/chatroom')

class Login(MethodView):
    def post(self):
        username = request.form['email']
        password = request.form['password'].encode('utf-8')

        connect = sqlite3.connect("misc/main_db")
        cur = connect.cursor()
        cur.execute("SELECT password FROM logins WHERE username = ?", (username,))
        result = cur.fetchone()

        if result and bcrypt.checkpw(password, result[0]):
            cur.close()
            session['username'] = username
            return redirect('/chatroom')
        else:
            return "Login Failed"

class SendMessage(MethodView):
    def post(self):
        username = session.get('username')
        message = request.form['message']

        conn = sqlite3.connect("misc/chat.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO messages (username, message) VALUES (?, ?)", (username, message))
        conn.commit()
        conn.close()

        return "Message sent"

class GetMessages(MethodView):
    def get(self):
        conn = sqlite3.connect("misc/chat.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM messages")
        messages = cursor.fetchall()
        conn.close()

        formatted_messages = ""
        for msg in messages:
            formatted_messages += f"{msg[1]}: {msg[2]}<br>"

        return formatted_messages

if __name__ == '__main__':
    app = ChatApp()
    app.run(host='0.0.0.0')
