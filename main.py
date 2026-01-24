from modules.passwords import hashing, verify
import os
import json
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify
from markupsafe import escape
from modules.db import User, Drive, Passenger
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, update, delete, create_engine, URL, Null, and_
from functools import wraps

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


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'name' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def serialize_drive(drive):
    return {
        "id_drive": drive.id_drive,
        "organizer": drive.organizer,
        "date": drive.date,
        "time": drive.time,
        "price": float(drive.price) if drive.price != Null else 0,
        "seat_amount": drive.seat_amount,
        "start_street": drive.start_street,
        "start_house_number": drive.start_house_number,
        "start_postal_code": drive.start_postal_code,
        "start_place": drive.start_place,
        "end_street": drive.end_street,
        "end_house_number": drive.end_house_number,
        "end_postal_code": drive.end_postal_code,
        "end_place": drive.end_place,
        "osmlink": drive.osmlink
    }

def filter_drives(
    organizer=None,
    date=None,
    time=None,
    price_min=None,
    price_max=None,
    start_postal_code=None,
    start_place=None,
    end_postal_code=None,
    end_place=None
):
    """
    Filters drives directly from the database using SQLAlchemy.
    
    Returns a list of Drive objects matching the criteria.
    """
    stmt = select(Drive)

    filters = []

    if organizer:
        filters.append(Drive.organizer.ilike(f"%{organizer}%"))  # partial match
    if date:
        if isinstance(date, str):
            date = datetime.strptime(date, "%Y-%m-%d").date()
        filters.append(Drive.date == date)
    if time:
        if isinstance(time, str):
            time = datetime.strptime(time, "%H:%M").time()
        filters.append(Drive.time == time)
    if price_min is not None:
        filters.append(Drive.price >= price_min)
    if price_max is not None:
        filters.append(Drive.price <= price_max)
    if start_postal_code:
        filters.append(Drive.start_postal_code == start_postal_code)
    if start_place:
        filters.append(Drive.start_place.ilike(f"%{start_place}%"))
    if end_postal_code:
        filters.append(Drive.end_postal_code == end_postal_code)
    if end_place:
        filters.append(Drive.end_place.ilike(f"%{end_place}%"))

    if filters:
        stmt = stmt.where(and_(*filters))

    drives = session_db.execute(stmt).scalars().all()
    return drives

    

#----- Routes -----
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():    
    stmt = select(Drive).where(Drive.organizer != session['name']).limit(5)
    my_drives = session_db.execute(stmt).scalars().all()
    my_drives: str = jsonify([serialize_drive(drive) for drive in my_drives]).get_data(as_text=True)
    return render_template('home.html', my_drives=my_drives)

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == 'POST':
        organizer: str = escape(request.form.get('organizer', ''))
        date: str = escape(request.form.get('date', ''))
        time: str = escape(request.form.get('time', ''))
        price_min: str = escape(request.form.get('price_min', ''))
        price_max: str = escape(request.form.get('price_max', ''))
        start_postal_code: str = escape(request.form.get('start_postal_code', ''))
        start_place: str = escape(request.form.get('start_place', ''))
        end_postal_code: str = escape(request.form.get('end_postal_code', ''))
        end_place: str = escape(request.form.get('end_place', ''))
        filtered_drives = filter_drives(organizer=organizer if organizer else None,
                      date=date if date else None,
                      time=time if time else None,
                      price_min=float(price_min) if price_min else None,
                      price_max=float(price_max) if price_max else None,
                        start_postal_code=start_postal_code if start_postal_code else None,
                        start_place=start_place if start_place else None,
                        end_postal_code=end_postal_code if end_postal_code else None,
                        end_place=end_place if end_place else None)
        for drive in filtered_drives:
            serialize_drive(drive)
        drives_list = filtered_drives
        return render_template('search.html', drives=drives_list)
    return render_template('search.html')

@app.route('/create_route', methods=['GET', 'POST'])
@login_required
def create_route():
    if request.method == 'POST':
        stmt = select(User).where(User.email.in_([session['email']]))
        column_data = session_db.execute(stmt).scalar_one_or_none()
        date: str = escape(request.form['date'])
        time: str = escape(request.form['time'])
        price: float = float(escape(request.form['price']))
        seats: int = int(escape(request.form['seats']))

        start_street: str = escape(request.form['start_street'])
        start_house_number: int = int(escape(request.form['start_house_number']))
        start_postal_code: int = int(escape(request.form['start_postal_code']))
        start_place: str = escape(request.form['start_place'])

        end_street: str = escape(request.form['end_street'])
        end_house_number: int = int(escape(request.form['end_house_number']))
        end_postal_code: int = int(escape(request.form['end_postal_code']))
        end_place: str = escape(request.form['end_place'])
        drive = Drive(organizer=column_data.name, date=date, time=time, price=price, seat_amount=seats, start_street=start_street, start_house_number=start_house_number, start_postal_code=start_postal_code, start_place=start_place, end_street=end_street, end_house_number=end_house_number, end_postal_code=end_postal_code, end_place=end_place)
        session_db.add(drive)
        session_db.commit()
        flash("Die Fahrt wurde erfolgreich hinzugefügt")
        return render_template('home.html')
    return render_template('create_route.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email: str = escape(request.form['email'])
        password: str = escape(request.form['password'])
        stmt = select(User).where(User.email.in_([email]))
        column_data = session_db.execute(stmt).scalar_one_or_none()
        try:
            column_data.email
        except AttributeError:
            flash("User does not exists")
            return render_template('login.html')
        else:
            if verify(column_data.password_hash, password):
                session['email'] = column_data.email
                session['name'] = column_data.name
                return redirect(url_for('home'))
            else:
                flash("Incorrect password")
                return render_template('login.html')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username: str = escape(request.form['username'])
        email: str = escape(request.form['email'])
        password: str = escape(request.form['password'])
        password2: str = escape(request.form['password2'])
        if password == password2 and not session_db.execute(select(User).where(User.email.in_([email]))).scalar_one_or_none() and not session_db.execute(select(User).where(User.name.in_([username]))).scalar_one_or_none():
            password_hash = hashing(password)
            user = User(name=username, email=email, password_hash=password_hash)
            session_db.add(user)
            session_db.commit()
            flash("registration successful, please log in")
            return redirect(url_for('login'))
        else:
            flash("passwords do not match or your email is already in use")
            return render_template('register.html')
    return render_template('register.html')


@app.route('/mydrives', methods=['GET', 'POST'])
@login_required
def my_drives():
        stmt = select(Drive).where(Drive.organizer == session['name'])
        my_drives = session_db.execute(stmt).scalars().all()
        my_drives = json.dumps([drive.__dict__ for drive in my_drives], default=str)
        return render_template('my_drives.html', my_drives=my_drives)

@app.route('/drive/<int:id>', methods=['GET'])
@login_required
def get_drive_route(id):
        return render_template('drive.html', drive_id=id)

@app.route("/passenger", methods=['GET'])
@login_required
def passenger():
    if request.method == 'GET':
        return render_template('passenger.html')
        
    
@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        old_password:str = escape(request.form["password-old"])
        new_password: str = escape(request.form["password-new"])
        stmt = select(User).where(User.email.in_([session['email']]))
        column_data = session_db.execute(stmt).scalar_one_or_none()
        password_hash = column_data.password_hash
        if verify(password_hash, old_password):
            p2 = hashing(new_password)
            new_password_hash = p2
            upd = update(User).where(User.email.in_([session['email']])).values(password_hash=new_password_hash)
            session_db.execute(upd)
            session_db.commit()
            return render_template('settings.html')
        else:
            flash("Altes Passwort ist falsch")
    return render_template('settings.html')

@app.errorhandler(404)
def not_found(e):
  return render_template("404.html")


#----- API Routes -----

@app.route('/api/all_drives', methods=['GET'])
@login_required
def all_drives():
        stmt = select(Drive).where(Drive.organizer != session['name'] and Drive.seat_amount > 0)
        drives = session_db.execute(stmt).scalars().all()
        drives_list = []
        for drive in drives:
            drives_list.append(serialize_drive(drive))
        return jsonify(drives_list), 200

@app.route('/api/my_drives', methods=['GET'])
@login_required
def api_my_drives():
    if request.method != 'GET':
        return jsonify({"error": "Invalid request method"}), 405
    if request.method == 'GET':
        stmt = select(Drive).where(Drive.organizer == session['name'])
        drives = session_db.execute(stmt).scalars().all()
        drives_list = []
        for drive in drives:
            drives_list.append(serialize_drive(drive))
        return jsonify(drives_list), 200

@app.route('/api/drive/passenger/<int:id>', methods=['POST'])
@login_required
def add_passenger(id):
    drive = session_db.get(Drive, id)

    if session['name'] == drive.organizer:
        return jsonify({"error": "Organizer cannot be a passenger"}), 400
    if drive.seat_amount <= 0:
        return jsonify({"error": "No seats available"}), 400
    if session_db.execute(select(Passenger).where(Passenger.drive_id == id, Passenger.passenger_name == session['name'])).scalar_one_or_none():
        return jsonify({"message": "You are already a passenger"}), 300
    else:
        passenger = Passenger(drive_id=id, passenger_name=session['name'])
        session_db.add(passenger)
        session_db.commit()
        drive.seat_amount -= 1
        session_db.commit()
        return jsonify({"status": "success", "message": "Passenger added"}), 200



@app.route('/api/drive/delete/<int:id>', methods=['GET'])
@login_required
def delete_drive(id):
        organizer = session['name']
        stmt = select(Drive).where(Drive.id_drive == id)
        if session_db.execute(stmt).scalar_one_or_none().organizer == organizer:
            stmt = delete(Drive).where(Drive.id_drive == id)
            session_db.execute(stmt)
            session_db.commit()
            flash("Die Fahrt wurde erfolgreich gelöscht")
            return redirect(url_for('home'))
        return render_template('drive.html', drive_id=id)

@app.route('/api/drive/<int:id>', methods=['GET', 'PUT'])
@login_required
def drive_api(id):
    if request.method == 'GET':
        stmt = select(Drive).where(Drive.id_drive == id)
        drive = session_db.execute(stmt).scalar_one_or_none()

        if not drive:
            return jsonify({"error": "Drive not found"}), 404

        return jsonify(serialize_drive(drive)), 200
    if request.method == 'PUT':
        drive = session_db.get(Drive, id)
        if not drive:
            return jsonify({"error": "Drive not found"}), 404

        if drive.organizer != session['name']:
            return jsonify({"error": "Unauthorized"}), 403

        data = request.get_json()

        for key, value in data.items():
            if hasattr(drive, key):
                setattr(drive, key, value)

        session_db.commit()

        return jsonify({
            "status": "success",
            "message": "Drive updated"
        }), 200

@app.route('/api/passenger/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def passenger_api(id):

    user_name = session['name']

    drive = session_db.get(Drive, id)
    if not drive:
        return jsonify({"error": "Drive not found"}), 404
    
    if request.method == 'GET':
        stmt = select(Passenger).where(Passenger.drive_id == id)
        passengers = session_db.execute(stmt).scalars().all()
        passenger_list = [passenger.passenger_name for passenger in passengers]

        return jsonify({
            "drive_id": id,
            "passengers": passenger_list
        }), 200

    if request.method == 'DELETE':
        stmt = (
            delete(Passenger)
            .where(
                Passenger.drive_id == id,
                Passenger.passenger_name == user_name
            )
        )

        result = session_db.execute(stmt)

        if result.rowcount == 0:
            return jsonify({"error": "Passenger not found"}), 404

        drive.seat_amount += 1
        session_db.commit()

        return jsonify({
            "status": "success",
            "message": "Passenger removed"
        }), 200
    if request.method == 'PUT':
        if user_name == drive.organizer:
            return jsonify({"error": "Organizer cannot be a passenger"}), 404

        if drive.seat_amount <= 0:
            return jsonify({"error": "No seats available"}), 400
        existing_passenger = session_db.execute(
            select(Passenger).where(
                Passenger.drive_id == id,
                Passenger.passenger_name == user_name
            )
        ).scalar_one_or_none()

        if existing_passenger:
            return jsonify({"error": "Already a passenger"}), 409

        passenger = Passenger(drive_id=id, passenger_name=user_name)

        session_db.add(passenger)
        drive.seat_amount -= 1
        session_db.commit()

        return jsonify({
            "status": "success",
            "message": "Passenger added"
        }), 200

@app.route("/api/user/passenger/")
@login_required
def get_passenger_drives():
    drive_list = []
    stmt2 = select(Passenger.drive_id).where(Passenger.passenger_name == session["name"])
    drive_ids = session_db.execute(stmt2).scalars().all()

    for drive_id in drive_ids:
        stmt = select(Drive).where(Drive.id_drive == drive_id)
        drive = session_db.execute(stmt).scalar_one_or_none()

        drive_list.append(serialize_drive(drive))
    return drive_list

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)