from flask import Flask, render_template, request, session

app = Flask(__name__)


@app.route('/')
def home():
    if 'username' in session:
        return f'Logged in as {session["username"]}'
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')
    
@app.route('/login', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    return render_template('settings.html')
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
