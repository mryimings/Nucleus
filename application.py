from flask import Flask, render_template, request
from warrant import Cognito

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login')
def login():
    print(request.form)
    return render_template('login.html')

@app.route('/code_registration')
def code_registration():
    return render_template('code_registration.html')

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

if __name__ == "__main__":
    app.debug = True
    app.run()