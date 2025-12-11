from modules.passwords import PW_HANDLER
from modules.database.db import insert_user, get_hashed_password_by_email

from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('home'))
    return render_template('index.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username: str = request.form['username']
        email: str = request.form['email']
        password: str = request.form['password']
        password2: str = request.form['password2']
        if get_hashed_password_by_email(email) is None and password == password2:
            p1 = PW_HANDLER(password)
            password_hash = p1.hashing()
            insert_user(email, username, password_hash)
            return render_template('register.html', error="Success")
        else:
            return render_template('register.html', error="passwords do not match or your email is already in use")
    return render_template('register.html')
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email: str = request.form['email']
        password: str = request.form['password']
        User = get_hashed_password_by_email(email)
        if User is None:
            return render_template('login.html', error="User does not exists")
        else:
            p1 = PW_HANDLER(password)
            if p1.verify(User[2], password):
                session['username'] = email
                return redirect(url_for('home'))
        return render_template('index.html')
    return render_template('login.html')

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    return render_template('settings.html')
    
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
