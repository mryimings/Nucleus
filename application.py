from flask import Flask, render_template, redirect, url_for, flash, session, request
import logging
from logging.handlers import RotatingFileHandler
from warrant import Cognito

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
            app.logger.warning('Incorrect Username and password fot user (%s)', request.form.get('username'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/')
def welcome():
    if 'username' in session:
        return render_template('welcome.html', username=session['username'])
    else:
        return redirect(url_for('login'))

def valid_login(username, password):
    if username == password:
        return True
    else:
        return False

if __name__ == '__main__':
    app.debug = True
    app.secret_key = '\xe3-\xe1\xf7\xfb\x91\xb1\x8c\xae\xf2\xc1BH\xe0/K~~%>ac\t\x01'
    #logging
    handler = RotatingFileHandler('error.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run()