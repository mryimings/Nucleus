from flask import Flask, render_template, redirect, url_for, flash, session, request
import logging
from logging.handlers import RotatingFileHandler
from warrant import Cognito
from config import cognito_userpool_id, cognito_app_client_id
import traceback


app = Flask(__name__)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['password']):
            flash("Successfully logged in")
            session['username'] = request.form.get('username')
            return redirect(url_for('welcome'))
        else:
            error = 'Incorrect username and password'
            app.logger.warning('Incorrect Username and password for user (%s)', request.form.get('username'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', "POST"])
def signup():
    error = None
    if request.method == 'POST':
        cognito = Cognito(user_pool_id=cognito_userpool_id, client_id=cognito_app_client_id)
        cognito.add_base_attributes(email=request.form['email'])
        cognito.register(username=request.form['username'], password=request.form['password'])
        flash("Please check your inbox for verification code")
        session['username'] = request.form['username']
        return redirect(url_for('verification'))
    return render_template('signup.html', error=error)

@app.route('/verification', methods=['GET', 'POST'])
def verification():
    assert 'username' in session
    username = session['username']
    if request.method == 'POST':
        cognito = Cognito(user_pool_id=cognito_userpool_id, client_id=cognito_app_client_id, username=username)
        try:
            cognito.confirm_sign_up(confirmation_code=request.form['vcode'])
            return redirect(url_for('welcome'))
        except Exception as e:
            print(e)
            error = 'Unable to verify, please try again'
            return render_template('signup.html', error=error)

    return render_template("verification.html")

@app.route('/')
def welcome():
    if 'username' in session:
        return render_template('welcome.html', username=session['username'])
    else:
        return redirect(url_for('login'))

def valid_login(username, password):
    cognito = Cognito(cognito_userpool_id, cognito_app_client_id, username=username)
    try:
        cognito.authenticate(password)
    except Exception as e:
        print(e)
        return False
    return True

if __name__ == '__main__':
    app.debug = True
    app.secret_key = '\xe3-\xe1\xf7\xfb\x91\xb1\x8c\xae\xf2\xc1BH\xe0/K~~%>ac\t\x01'
    #logging
    handler = RotatingFileHandler('error.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run()