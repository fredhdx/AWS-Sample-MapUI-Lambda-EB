
from flask import flash, render_template, url_for, flash, redirect,request
from MapService import app, users, bcrypt, MAPBOX_ACCESS_TOKEN, MAPBOX_STYLE, DATABASE_NAME
from MapService.forms import RegistraionFrom, LoginForm, UpdateAccountForm
from MapService.models import User
from flask_login import login_user, logout_user, current_user, login_required
import requests
import json

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistraionFrom()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf8')
        user = {'username':form.username.data,
                'email':form.email.data,
                'password':hashed_password}
        users.insert_one(user)
        flash(f'Account created for {form.username.data}! You can log in now.', 'success')
        return redirect(url_for('login'))
    return render_template("register.html", title="Register", form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = users.find_one({"email": form.email.data})
        if user and bcrypt.check_password_hash(user['password'], form.password.data):
            login_user(User.get_user(form.email.data))
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'Login unsuccessful! Please, check your email and password.', 'danger')
    return render_template("login.html", title="Login", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        users.update_one({"email": form.email.data}, {'$set': {
            'username': current_user.username,
            'email':current_user.email}})
        flash(f'Your account has been updated.', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    return render_template('account.html', title='Account', form=form)

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title="Home")


@app.route("/monitor_map", methods=['GET', 'POST'])
@login_required
def monitor_map():
    return render_template(
        "monitor_map.html", title="MapService",
        mapbox_access_token=MAPBOX_ACCESS_TOKEN,
        database_name=DATABASE_NAME,
        mapbox_style = MAPBOX_STYLE,
        current_user_email = current_user.email)

@app.route("/recommend", methods=["GET"])
def recommend():
    r = requests.get('https://59n15ppg2i.execute-api.us-west-1.amazonaws.com/dev/recommend')
    response = json.dumps(r.json(), sort_keys = True, indent = 4, separators = (',', ': '))
    return render_template("monkey.html", response=response)
