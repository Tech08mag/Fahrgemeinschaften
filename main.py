from modules.passwords import PW_HANDLER
import os
import json
from dotenv import load_dotenv
from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify
from modules.db import User, Drive, Passenger
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, insert, update, delete, create_engine, URL

url_object = URL.create(
    "postgresql+psycopg2",
    username=os.getenv("PG_USERNAME"),
    password=os.getenv("PG_PASSWORD"),
    host=os.getenv("PG_HOST", "postgres"),
    database=os.getenv("PG_DATABASE"),
)

engine = create_engine(url_object, echo=True)
Session: sessionmaker[engine] = sessionmaker(bind=engine)
session_db = Session()

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_route', methods=['GET', 'POST'])
def create_route():
    if 'name' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        stmt = select(User).where(User.email.in_([session['email']]))
        column_data = session_db.execute(stmt).scalar_one_or_none()
        date: str = request.form['date']
        time: str = request.form['time']
        price: float = float(request.form['price'])
        seats: int = int(request.form['seats'])
        startpoint: str = request.form['startpoint']
        destination: str = request.form['destination']
        drive = Drive(organizer=column_data.name, date=date, time=time, price=price, seat_amount=seats, startpoint=startpoint, destination=destination)
        session_db.add(drive)
        session_db.commit()
        flash("Die Fahrt wurde erfolgreich hinzugefügt")
        return render_template('index.html')
    return render_template('create_route.html')

@app.route('/mydrives', methods=['GET', 'POST'])
def my_drives():
    if 'name' not in session:
        return redirect(url_for('login'))
    else:
        stmt = select(Drive).where(Drive.organizer == session['name'])
        my_drives = session_db.execute(stmt).scalars().all()
        my_drives = json.dumps([drive.__dict__ for drive in my_drives], default=str)
        return render_template('my_drives.html', my_drives=my_drives)

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'name' not in session:
        return redirect(url_for('login'))
    else:
        stmt = select(Drive).where(Drive.organizer != session['name'])
        my_drives = session_db.execute(stmt).scalars().all()
        my_drives = json.dumps([drive.__dict__ for drive in my_drives], default=str)
        return render_template('home.html', my_drives=my_drives)

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
            user = User(name=username, email=email, password_hash=password_hash)
            session_db.add(user)
            session_db.commit()
            flash("registration successful, please log in")
            return redirect(url_for('login'))
        else:
            flash("passwords do not match or your email is already in use")
            return render_template('register.html')
    return render_template('register.html')
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email: str = request.form['email']
        password: str = request.form['password']
        stmt = select(User).where(User.email.in_([email]))
        column_data = session_db.execute(stmt).scalar_one_or_none()
        try:
            column_data.email
        except AttributeError:
            flash("User does not exists")
            return render_template('login.html')
        else:
            p1 = PW_HANDLER(password)
            if p1.verify(column_data.password_hash, password):
                session['email'] = column_data.email
                session['name'] = column_data.name
                return redirect(url_for('home'))
            else:
                flash("Incorrect password")
                return render_template('login.html')
    return render_template('login.html')

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if 'name' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        new_username: str = request.form["user"]
        old_password:str = request.form["password-old"]
        new_password: str = request.form["password-new"]
        stmt = select(User).where(User.email.in_([session['username']]))
        column_data = session_db.execute(stmt).scalar_one_or_none()
        password_hash = column_data.password_hash
        p1 = PW_HANDLER(old_password)
        if p1.verify(password_hash, old_password):
            p2 = PW_HANDLER(new_password)
            new_password_hash = p2.hashing()
            upd = update(User).where(User.email.in_([session['username']])).values(name=new_username, password_hash=new_password_hash)
            session_db.execute(upd)
            session_db.commit()
            return render_template('settings.html')
    return render_template('settings.html')

@app.route('/logout')
def logout():
    session.pop('name', None)
    session.pop('email', None)
    return redirect(url_for('index'))

@app.route('/api/all_drives', methods=['GET'])
def all_drives():
    stmt = select(Drive)
    all_drives = session_db.execute(stmt).scalars().all()
    all_drives = json.dumps([drive.__dict__ for drive in all_drives], default=str)
    return all_drives

@app.route('/api/my_drives', methods=['GET'])
def disp():
    if 'name' not in session:
        return 'not logged in try loggin in'
    else:
        stmt = select(Drive).where(Drive.organizer == session['name'])
        my_drives = session_db.execute(stmt).scalars().all()
        print(my_drives)
        my_drives = json.dumps([drive.__dict__ for drive in my_drives], default=str)
        print(my_drives)
    return my_drives

@app.route('/drive/<int:num>', methods=['GET'])
def drive(num):
    if 'name' not in session:
        return 'not logged in try loggin in'
    else:
        return render_template('drive.html', drive_id=num)

@app.route('/api/drive/<int:id>', methods=['GET', 'PUT'])
def drive_api(id):
    # Auth check
    if 'name' not in session:
        return jsonify({"error": "Not logged in"}), 401

    # ---------- PUT ----------
    if request.method == 'PUT':
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        drive = session_db.get(Drive, id)

        if not drive:
            return jsonify({"error": "Drive not found"}), 404

        # Optional: block updating primary key
        data.pop("id_drive", None)

        for field, value in data.items():
            if hasattr(drive, field):
                setattr(drive, field, value)

        session_db.commit()

        return jsonify({
            "status": "success",
            "drive": {
                "id_drive": drive.id_drive,
                "organizer": drive.organizer,
                "date": drive.date,
                "time": drive.time,
                "price": float(drive.price) if drive.price else None,
                "seat_amount": drive.seat_amount,
                "startpoint": drive.startpoint,
                "destination": drive.destination,
                "osmlink": drive.osmlink
            }
        }), 200

    # ---------- GET ----------
    stmt = select(Drive).where(Drive.id_drive == id)
    drive = session_db.execute(stmt).scalar_one_or_none()

    if not drive:
        return jsonify({"error": "Drive not found"}), 404

    return jsonify({
        "id_drive": drive.id_drive,
        "organizer": drive.organizer,
        "date": drive.date,
        "time": drive.time,
        "price": float(drive.price) if drive.price else None,
        "seat_amount": drive.seat_amount,
        "startpoint": drive.startpoint,
        "destination": drive.destination,
        "osmlink": drive.osmlink
    }), 200


@app.errorhandler(404)
def not_found(e):
  return render_template("404.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)