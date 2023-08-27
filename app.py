from flask import Flask, request, jsonify, render_template,flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, logout_user, login_required, current_user, LoginManager,UserMixin
import os
from oauthlib.oauth2 import WebApplicationClient
import json
import requests
import random
from datetime import datetime, timedelta

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

session = {}
secret_key = os.urandom(24)
app.config['SECRET_KEY'] = secret_key

with open('config.json', 'r') as f:
    params = json.load(f)["params"]

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

GOOGLE_CLIENT_ID = params["google_client_id"]
# GOOGLE_CLIENT_SECRET = params["google_client_secret"]
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)
client = WebApplicationClient(GOOGLE_CLIENT_ID)

session['url'] = "/"

@login_manager.user_loader


#for the locally run server outh2 need https but lo

def get_user(ident):
  return User.query.get(int(ident))
class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    email = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(50))
    role = db.Column(db.Integer)
    auth_type = db.Column(db.String(50))

    def __repr__(self):
        return '<User %r>' % self.name


class Medicine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    use_for = db.Column(db.String(50), nullable=False)
    def __repr__(self):
        return '<Medicine %r>' % self.name


class Prescription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, nullable=False)
    doctor_id = db.Column(db.Integer, nullable=False)
    medicine_id = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return '<Prescription %r>' % self.name

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, nullable=False)
    doctor_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(50), nullable=False)
    time = db.Column(db.Time, nullable=False)  # Change this field type
    symptoms = db.Column(db.String(50), nullable=False)  # Correct typo in field name
    def __repr__(self):
        return '<Appointment %r>' % self.id  # Correct repr method to show id



if not os.path.exists('database.db'):
    with app.app_context(): 
        db.create_all()



@app.route('/')
def index():
    
    if current_user.is_authenticated:
        session['url']="/"
        return render_template('home.html',user=current_user)
    session['url']="/"
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    session['url']="/login"
    if current_user.is_authenticated:
        return redirect("/")
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            if user.password == password:
                print('User authenticated')
                login_user(user)
                return redirect("/")
            else:
                return render_template('login.html', error='Incorrect password')
        else:
            return render_template('login.html', error='User does not exist')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('index.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    session['url']="/register"
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        auth_type = "local"
        if User.query.filter_by(username=username).first():
            return render_template('register.html', error='User already exists')
        
        if User.query.filter_by(email=email).first():
            return render_template('register.html', error='Email already exists')
        print(username, password, email)
        user = User(username=username, password=password, email=email, role=3, auth_type=auth_type)
        db.session.add(user)
        db.session.commit()
        print('User created')

        flash('Registration successful. You can now log in.', 'success')  

        return render_template('index.html')

    else:
        return render_template('register.html')



@app.route('/admin')
@login_required
def admin():
    if current_user.role == 1:
        return render_template('admin.html')
    else:
        return render_template('index.html')


@app.route('/doctor')
@login_required
def doctor():
    if current_user.role == 2:
        return render_template('doctor.html')
    else:
        return render_template('index.html')


@app.route('/patient')
@login_required
def patient():
    if current_user.role == 3:
        return render_template('patient.html')
    else:
        return render_template('index.html')



@app.route('/add_admin', methods=['POST'])
def add_admin():
    username = "admin"
    password = "admin"
    email = "admin@xyz.com"
    role = 1
    auth_type = "local"
    user = User(username=username, password=password, email=email, role=role, auth_type=auth_type)
    db.session.add(user)
    db.session.commit()
    return render_template('index.html')


@app.route('/add_doctor', methods=['POST'])
def add_doctor():
    username = "doctor"
    password = "doctor"
    email = "doc@doc.com"
    role = 2
    auth_type = "local"
    user = User(username=username, password=password, email=email, role=role, auth_type=auth_type)
    db.session.add(user)
    db.session.commit()
    return render_template('index.html')
    

#book apoitment
#healt record history
#doctor shcedule


#manage doctor
    #doctor list


#manage pharmacy

#view all patient

#all doctor schedual

#create summery of all doctor that how many patient they have seen at the end of the day to admin
#meeting with admin 
        

#add prescription by the doctor
@app.route('/add_prescription', methods=['POST'])
def add_prescription():

    if current_user.role != 2:
        return render_template('index.html')
    patient_id = request.form['patient_id']
    doctor_id = request.form['doctor_id']
    medicine_id = request.form['medicine_id']
    prescription = Prescription(patient_id=patient_id, doctor_id=doctor_id, medicine_id=medicine_id)
    db.session.add(prescription)
    db.session.commit()
    return render_template('doctor.html')


            

#add medicine by the admin
@app.route('/add_medicine', methods=['POST'])
def add_medicine():
    if current_user.role != 1:
        return render_template('index.html')
    name = request.form['name']
    use_for = request.form['use_for']
    medicine = Medicine(name=name, use_for=use_for)
    db.session.add(medicine)
    db.session.commit()
    return render_template('admin.html')





@app.route('/book_appointment', methods=['POST',"GET"])
def book_appointment():
    if not current_user.is_authenticated:
        return render_template('login.html', error='Please log in to book an appointment.')

    if request.method == 'POST':
        patient_id = current_user.id
        
        #find the free time of the doctor and make appointment on that time
       #don't take the time from the user

        # get the random doctor id
        doctor_id = 0

        last_appointment = Appointment.query.filter_by(doctor_id=doctor_id).order_by(Appointment.id.desc()).first()

        
        # no appointment found then start from 9
        if last_appointment == None:
            time = datetime.strptime("09:00", "%H:%M").time()
        else:
            last_appointment_time = last_appointment.time
            last_appointment_datetime = datetime.strptime(last_appointment_time, "%H:%M")
            new_time = last_appointment_datetime + timedelta(minutes=30)
            time = new_time.time()
        
        #data is todays date

        date = datetime.now().strftime("%d/%m/%Y")
        
        symptoms = request.form['symptoms']

        appointment = Appointment(patient_id=patient_id, doctor_id=doctor_id, date=date, time=time, symptoms=symptoms)

        db.session.add(appointment)
        db.session.commit()
        return render_template('home.html', user=current_user, message="Appointment booked successfully")
    else:
        doctors = User.query.filter_by(role=2).all()
        return render_template('book_appointment.html', doctors=doctors)












@app.route('/get_suggestions', methods=['GET'])
def get_suggestions():
    query = request.args.get('query')
    suggestions = []

    if query:
        medicines = Medicine.query.filter(Medicine.name.ilike(f'%{query}%')).limit(5)
        suggestions = [medicine.name for medicine in medicines]

    return render_template('suggestions.html', suggestions=suggestions)

@app.route('/get_patient', methods=['GET'])
def get_patient():
    query = request.args.get('query')
    suggestions = []

    if query:
        patients = User.query.filter(User.name.ilike(f'%{query}%')).limit(5)
        suggestions = [patient.name for patient in patients]

    return render_template('suggestions.html', suggestions=suggestions)





@app.route('/manage_doctor', methods=['GET'])
def manage_doctor():
    doctors = User.query.filter_by(role=2).all()
    return render_template('manage_doctor.html', doctors=doctors)











def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

@app.route("/login/google")
def google_login():
    google_provider_cfg = get_google_provider_cfg()
    auth_endpoint = google_provider_cfg["authorization_endpoint"]

    request_uri = client.prepare_request_uri(
        auth_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],

    )
    

    return redirect(request_uri)

@app.route("/login/google/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url="http://127.0.0.1:5000/login/google/callback",
        code=code,
    )

    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(params["google_client_id"], params["google_client_secret"]),
    )
    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    userinfo_data = userinfo_response.json()

    if userinfo_response.json().get("email_verified"):
        users_email = userinfo_data["email"]
        user = User.query.filter_by(email=users_email).first()

        if user:
            if user.auth_type == "google":
                login_user(user)
                return redirect(session['url'])
            else:
                return render_template('home.html', user=current_user)
        else:
            # Create a new user using Google account information
            username = userinfo_data.get("name", "Google User")
            auth_type = "google"
            role = 3
            user = User(username=username, email=users_email, auth_type=auth_type, role=role)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(session['url'])
    else:
        return "User email not available or not verified by Google.", 400













@app.route('/test')
def test():
    return render_template('Appointment.html')














if __name__ == '__main__':
    app.run(debug=True)
    