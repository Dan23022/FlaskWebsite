import os
import sqlite3
import bcrypt
from flask import Flask, render_template, request, redirect, session, jsonify
from flask.views import MethodView

class ChatApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'your-secret-key'
        self.chat_messages = {}

    def setup_routes(self):
        self.app.add_url_rule('/', view_func=LoginPage.as_view('login_page'))
        self.app.add_url_rule('/register', view_func=LoginPage.as_view('register'))
        self.app.add_url_rule('/login', view_func=Login.as_view('login'))
        self.app.add_url_rule('/chatroom', view_func=ChatRoom.as_view('chatroom'))
        self.app.add_url_rule('/send_message', view_func=SendMessage.as_view('send_message'))
        self.app.add_url_rule('/get_messages', view_func=GetMessages.as_view('get_messages'))

    def run(self):
        self.setup_routes()
        self.app.run(debug=True)

class ChatRoom(MethodView):
    def get(self):
        return render_template('chatroom.html')

class LoginPage(MethodView):
    def get(self):
        return render_template('login_page.html')

    def post(self):
        username = request.form['email']
        password = request.form['password'].encode('utf-8')

        connect = sqlite3.connect(f"misc/main_db")
        cur = connect.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS logins (username TEXT, password TEXT)")
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
        cur.execute("INSERT INTO logins (username, password) VALUES (?, ?)", (username, hashed_password))
        connect.commit()

        session['username'] = username

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
        message = f"{session['username']}: {request.form['message']}"
        if 'messages' not in session:
            session['messages'] = []
        session['messages'].append(message)
        session.modified = True  # Explicitly mark the session as modified
        return "Message sent"

class GetMessages(MethodView):
    def get(self):
        if 'messages' in session:
            messages = "<br>".join(session['messages'])
        else:
            messages = ""
        return messages

if __name__ == '__main__':
    app = ChatApp()
    app.debug = True
    app.run()