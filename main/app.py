from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, logout_user, login_required, current_user, LoginManager
import os
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.Integer, nullable=False)
    mobile = db.Column(db.Integer, nullable=False)
    password = db.Column(db.Integer)
    role = db.Column(db.Integer)
    def __repr__(self):
        return '<User %r>' % self.name


class Medicine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    use_for = db.Column(db.String(50), nullable=False)
    def __repr__(self):
        return '<Medicine %r>' % self.name



if not os.path.exists('database.db'):
    with app.app_context(): 
        db.create_all()



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(name=username, password=password).first()
        if user:
            if user.password == password:
                login_user(user)
                return render_template('index.html')
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
        mobile = request.form['mobile']
        user = User(name=username, password=password, email=email, mobile=mobile)
        db.session.add(user)
        db.session.commit()
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
    