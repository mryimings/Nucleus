from flask import Flask, render_template, redirect, url_for, flash, session, request
import logging
from logging.handlers import RotatingFileHandler
from warrant import Cognito
from config import cognito_userpool_id, cognito_app_client_id
from models.r_net.inference import Inference
import wikipedia
from rake_nltk import Rake
from database.db_update_class import db
from datetime import datetime

inference = Inference()

app = Flask(__name__)
database = db()

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
        if len(request.form['password']) < 8:
            error = 'Password too short!'
        else:
            cognito = Cognito(user_pool_id=cognito_userpool_id, client_id=cognito_app_client_id)
            cognito.add_base_attributes(email=request.form['email'])
            try:
                cognito.register(username=request.form['username'], password=request.form['password'])
                user_id = database.add_user(request.form['username'],request.form['password'],request.form['email'])
            except Exception as e:
                print(e)
                error = str(e)
                return render_template('signup.html', error=error)
            flash("Please check your inbox for verification code")
            session['username'] = request.form['username']
            return redirect(url_for('verification'))
    return render_template('signup.html', error=error)


@app.route('/verification', methods=['GET', 'POST'])
def verification():
    if 'username' in session:
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
    else:
        return redirect(url_for('login'))


@app.route('/', methods=['GET', 'POST'])
def welcome():
    if 'username' in session:
        return render_template('welcome.html', username=session['username'])
    else:
        return redirect(url_for('login'))

@app.route('/with_context', methods=['GET', 'POST'])
def with_context():
    if 'username' in session:
        if request.method == 'POST':
            # flash(inference.response(context=request.form['passage'], question=request.form['question']))
            user_id = database.get_id_by_name(session['username'])
            keyword = str(datetime.now())
            database.update(user_id,keyword,request.form['passage'],request.form['question'])
            question = request.form['question']
            passage = request.form['passage']
            answer = inference.response(context=passage, question=question)
            return redirect(url_for('result', question=question, answer=answer))
        return render_template('with_context.html', username=session['username'])
    else:
        return redirect(url_for('login'))

@app.route('/without_context', methods=['GET', 'POST'])
def without_context():
    if 'username' in session:
        if request.method == 'POST':
            rake = Rake()
            rake.extract_keywords_from_text(request.form['question'])
            keywords = rake.get_ranked_phrases()
            keyword = keywords[0]
            passage = wikipedia.page(keyword).summary
            answer = inference.response(passage, question=request.form['question'])
            # flash("The answer of your question is: {}".format(answer))
            user_id = database.get_id_by_name(session['username'])
            database.update(user_id,keyword,passage,request.form['question'])
            return redirect(url_for('result', question=request.form['question'], answer=answer))
        else:
            return render_template('without_context.html', username=session['username'])
    else:
        return redirect(url_for('login'))

@app.route('/result/<question>/<answer>', methods=['GET', 'POST'])
def result(question="", answer=""):
    if 'username' in session:
        print("Question", question)
        print("Answer", answer)
        return render_template('result.html', username=session['username'], question=question, answer=answer)
    else:
        return redirect(url_for('login'))

@app.route('/satisfied/<question>/<answer>', methods=['GET', 'POST'])
def satisfied(question="", answer=""):
    if 'username' in session:
        print("Satisfied Question:", question)
        print("Satisfied Answer:", answer)
        # TODO: save it to database
        return render_template('satisfied.html', username=session['username'], question=question, answer=answer)
    else:
        return redirect(url_for('login'))

@app.route('/unsatisfied/<question>/<answer>', methods=['GET', 'POST'])
def unsatisfied(question="", answer=""):
    if 'username' in session:
        if request.method == 'GET':
            print("Method: GET. Unsatisfied Question:", question)
            print("Method: GET. Unsatisfied Answer:", answer)
            return render_template('unsatisfied.html', username=session['username'], question=question, answer=answer)
        else:
            print("Method: POST. Unsatisfied Question:", question)
            print("Method: POST. Unsatisfied Answer:", answer)
            print("Method: POST. Unsatisfied expected_answer:", request.form['expected_answer'])
            flash("Your feedback has been recorded! Thank you for helping us improving Nucleus!")
            # TODO: save it to database
            return redirect(url_for('unsatisfied_result'))
    else:
        return redirect(url_for('login'))
    
@app.route('/history/', methods=['GET', 'POST'])
def history():
    if 'username' in session:
        if request.method == 'POST':
            num = request.form['num']
            requested_history = database.get_history_list(name=session['username'], limit=num)
            # TODO: send history to frontend
            return "TO DO"
        else:
            return render_template('history.html', username=session['username'])
    else:
        return redirect(url_for('login'))
    
    
@app.route('/feedback/<question>/<answer>', methods=['GET', 'POST'])
def feedback(question=None, answer=None):
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        database.user_feedback(session['username'], question, answer, int(request.form['score']),
                               request.form['expected_answer'])
        return redirect(url_for("welcome", username=session['username']))
    else:
        return render_template('feedback.html', username=session['username'], question=question, answer=answer)

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
    app.run()
    
