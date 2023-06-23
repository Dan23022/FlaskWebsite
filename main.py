from flask import *

app = Flask(__name__)

@app.route('/')
def login_page():
    return render_template('login_page.html')

@app.route('/register', methods=['POST'])
def register():
    print('register')
    username = request.form['email']
    password = request.form['password']

    return "Registration Successful"

@app.route('/login', methods=['POST'])
def login():
    print('login')
    username = request.form['email']
    password = request.form['password']

    if username == "test":
        return "Login Successful"
    else:
        return "Login Failed"

if __name__ == '__main__':
    app.run(debug=True)
