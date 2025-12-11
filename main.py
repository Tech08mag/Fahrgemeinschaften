from modules.passwords import PW_HANDLER
from modules.database.db import insert_user

from flask import Flask, render_template, request

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username: str = request.form['username']
        email: str = request.form['email']
        password: str = request.form['password']
        password2: str = request.form['password2']
        if password == password2:
            p1 = PW_HANDLER(password)
            password_hash = p1.hashing()
            insert_user(email, username, password_hash)
            return render_template('register.html', error="wrong password")
        else:
            return render_template('register.html', error="wrong password")
    return render_template('register.html')
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        p1 = PW_HANDLER(password)
        password_hash = p1.hashing()
        print(f'Username: {username}')
        print(f'Password: {password_hash}')
        return render_template('index.html')
    return render_template('login.html')

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    return render_template('settings.html')
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
