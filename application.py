import os

from flask import Flask, render_template, redirect, url_for, flash, request
from passlib.hash import pbkdf2_sha256
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename
import pandas as pd

from forms_fiels import *
from models import *
from project import *

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET')

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['UPLOAD_FOLDER'] = 'myfolder'

db = SQLAlchemy(app)

login = LoginManager(app)
login.init_app(app)


@login.user_loader
def load_user(id):
    
    return User.query.get(int(id))

@app.route("/", methods = ['GET', 'POST'])
def index():

    reg_form = Registration()

    if reg_form.validate_on_submit():
        
        username = reg_form.username.data
        password = reg_form.password.data

        hashed_password = pbkdf2_sha256.hash(password)

        user = User(username = username, password = hashed_password)
        db.session.add(user)
        db.session.commit()

        flash("Registered Successfully!!", 'success')

        return redirect(url_for('login'))

    return render_template('index.html', form = reg_form)

@app.route("/login", methods = ['GET', 'POST'])
def login():

    login_form = LoginForm()

    if login_form.validate_on_submit():
        
        user_object = User.query.filter_by(username = login_form.username.data).first()
        login_user(user_object)

        return redirect(url_for('main'))

    return render_template("login.html", form = login_form)


@app.route("/main", methods = ['GET', 'POST'])
#@login_required
def main():

    if not current_user.is_authenticated:

        flash("Please Login", 'danger')
        return redirect(url_for('login'))

    return render_template("main.html")

@app.route("/logout", methods = ['GET', 'POST'])
def logout():

    logout_user()
    flash("Logged out successfully!!", 'success')

    return render_template("logout.html")

@app.route('/success', methods=['GET', 'POST'])
def success():

    if request.method == 'POST':

        f = request.files['file']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))

        l = 'myfolder/{}'.format(f.filename)

        email = request.form.get("email")
        password = request.form.get("password")

        return readfile(l, email, password)

    return render_template("main.html")

@app.route('/success1', methods=['GET', 'POST'])
def success1():

    if request.method == 'POST':
        
        f = request.files['file']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))

        l = 'myfolder/{}'.format(f.filename)

        email = request.form.get("email")
        password = request.form.get("password")

        return readfile1(l, email, password)

    return render_template("main.html")

@app.route('/success2', methods=['GET', 'POST'])
def success2():

    if request.method == 'POST':

        f1 = request.files['file1']
        f1.save(os.path.join(app.config['UPLOAD_FOLDER'], f1.filename))
        f2 = request.files['file2']
        f2.save(os.path.join(app.config['UPLOAD_FOLDER'], f2.filename))

        l1 = 'myfolder/{}'.format(f1.filename)
        l2 = 'myfolder/{}'.format(f2.filename)

        email = request.form.get("email")
        password = request.form.get("password")

        return arrangement(l1, l2, email, password)

    return render_template("main.html")

@app.route('/ia1', methods=['GET', 'POST'])
def ia1():

    if request.method == 'POST':

        return render_template("ia1.html")

@app.route('/ia1and2', methods=['GET', 'POST'])
def ia1and2():

    if request.method == 'POST':

        return render_template("ia1and2.html")

@app.route('/iaarrangement', methods=['GET', 'POST'])
def iaarrangement():

    if request.method == 'POST':

        return render_template("iaarrangement.html")

if __name__ == "__main__":

    app.run(debug = True)