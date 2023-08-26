from flask import Flask, request, jsonify, render_template,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, logout_user, login_required, current_user, LoginManager,UserMixin
import os
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

secret_key = os.urandom(24)
app.config['SECRET_KEY'] = secret_key

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
@login_manager.user_loader


def get_user(ident):
  return User.query.get(int(ident))
class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(50))
    role = db.Column(db.Integer)
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



if not os.path.exists('database.db'):
    with app.app_context(): 
        db.create_all()



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return render_template('home.html',user=current_user)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(username, password)
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            print(user.password)
            print(type(password))
            print(type(user.password))
            if user.password == password:
                print('User authenticated')
                login_user(user)
                return render_template('home.html',user=current_user)
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
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if User.query.filter_by(username=username).first():
            return render_template('register.html', error='User already exists')
        
        if User.query.filter_by(email=email).first():
            return render_template('register.html', error='Email already exists')
        print(username, password, email)
        user = User(username=username, password=password, email=email, role=3)
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






if __name__ == '__main__':
    app.run(debug=True)
    