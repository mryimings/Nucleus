from flask import Flask, render_template, redirect, url_for, flash, session, request
import logging
from logging.handlers import RotatingFileHandler
from warrant import Cognito
from config import cognito_userpool_id, cognito_app_client_id
from models.bert.inference_bert import Inference
import wikipedia
from rake_nltk import Rake
from database.db_update_class import db
from datetime import datetime
from wikipedia.exceptions import PageError

inference = Inference()

app = Flask(__name__)
database = db()

keyword_topk = 5

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['password']):
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
            user_id = database.get_id_by_name(session['username'])
            database.update(user_id,str(datetime.now()),request.form['passage'],request.form['question'])
            
            question = request.form['question']
            passage = request.form['passage']
            result = inference.response(qas={"question": question,
                                             "context_list": [passage]})
            answer, _ = result[0][0], result[0][1]
            
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
            keywords = rake.get_ranked_phrases()[:keyword_topk]
            context_list = []
            for keyword in keywords:
                try:
                    passage = wikipedia.page(keyword).summary
                except PageError as e:
                    print("page not fund")
                    print(e)
                    continue
                context_list += get_context_list(passage)
            
            
            if not context_list:
                return redirect(url_for('result_no_answer'))
            
            feed_dict = {"question": request.form["question"], "context_list": context_list}
            results = inference.response(qas=feed_dict)
            final_answer = ""
            max_score = float("-inf")
            final_passage = ""
            for i, result in enumerate(results):
                answer, score = result
                if score > max_score:
                    max_score = score
                    final_answer = answer
                    final_passage = context_list[(i//3)]
            
            
            if not final_answer:
                return redirect(url_for('result_no_answer'))
            
            print("******************** Begins Logging **************************")
            
            for i, context in enumerate(context_list):
                print("context {}".format(str(i)))
                print(context)
            
            for i, result in enumerate(results):
                print('result {} for context {}'.format(str(i), str(i//3)))
                print("score {}".format(str(result[1])))
                print("answer {}".format(str(result[0])))
                
            user_id = database.get_id_by_name(session['username'])
            database.update(user_id, str(datetime.now()), final_passage, request.form['question'])
            
            return redirect(url_for('result', question=request.form['question'], answer=final_answer))
        
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
    
@app.route('/result_no_answer/', methods=['GET', 'POST'])
def result_no_answer(question=""):
    if 'username' in session:
        print("Question", question)
        return render_template('result_no_answer.html', username=session['username'])
    else:
        return redirect(url_for('login'))

@app.route('/history', methods=['GET', 'POST'])
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
        return redirect(url_for("thankyou", username=session['username']))
    else:
        return render_template('feedback.html', username=session['username'], question=question, answer=answer)
    
@app.route('/thankyou', methods=['GET'])
def thankyou():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('thankyou.html', username=session['username'])

def valid_login(username, password):
    cognito = Cognito(cognito_userpool_id, cognito_app_client_id, username=username)
    try:
        cognito.authenticate(password)
    except Exception as e:
        print(e)
        return False
    return True

def get_context_list(context, min_len=700):
    context_list = []
    assert context
    p1, p2 = 0, 0
    while p2 < len(context):
        p2 += min_len
        while p2 < len(context) and context[p2] != '.':
            p2 += 1
        p2 += 1
        context_list.append(context[p1:p2])
        p1 = p2
    return context_list

if __name__ == '__main__':
    app.debug = True
    app.secret_key = '\xe3-\xe1\xf7\xfb\x91\xb1\x8c\xae\xf2\xc1BH\xe0/K~~%>ac\t\x01'
    app.run()
    # print(get_context_list('''The City of New York, often called New York City (NYC) or simply New York (NY), is the most populous city in the United States. With an estimated 2017 population of 8,622,698 distributed over a land area of about 302.6 square miles (784 km2), New York City is also the most densely populated major city in the United States. Located at the southern tip of the state of New York, the city is the center of the New York metropolitan area, the largest metropolitan area in the world by urban landmass and one of the world's most populous megacities, with an estimated 20,320,876 people in its 2017 Metropolitan Statistical Area and 23,876,155 residents in its Combined Statistical Area. A global power city, New York City has been described uniquely as the cultural, financial, and media capital of the world, and exerts a significant impact upon commerce, entertainment, research, technology, education, politics, tourism, art, fashion, and sports. The city's fast pace has inspired the term New York minute. Home to the headquarters of the United Nations, New York is an important center for international diplomacy.Situated on one of the world's largest natural harbors, New York City consists of five boroughs, each of which is a separate county of the State of New York. The five boroughs – Brooklyn, Queens, Manhattan, The Bronx, and Staten Island – were consolidated into a single city in 1898. The city and its metropolitan area constitute the premier gateway for legal immigration to the United States. As many as 800 languages are spoken in New York, making it the most linguistically diverse city in the world. New York City is home to more than 3.2 million residents born outside the United States, the largest foreign-born population of any city in the world.  In 2017, the New York metropolitan area produced a gross metropolitan product (GMP) of US$1.73 trillion. If greater New York City were a sovereign state, it would have the 12th highest GDP in the world.New York City traces its origins to a trading post founded by colonists from the Dutch Republic in 1624 on Lower Manhattan; the post was named New Amsterdam in 1626. The city and its surroundings came under English control in 1664 and were renamed New York after King Charles II of England granted the lands to his brother, the Duke of York. New York served as the capital of the United States from 1785 until 1790. It has been the country's largest city since 1790. The Statue of Liberty greeted millions of immigrants as they came to the Americas by ship in the late 19th and early 20th centuries and is a world symbol of the United States and its ideals of liberty and peace. In the 21st century, New York has emerged as a global node of creativity and entrepreneurship, social tolerance, and environmental sustainability, and as a symbol of freedom and cultural diversity.Many districts and landmarks in New York City are well known, with the city having three of the world's ten most visited tourist attractions in 2013 and receiving a record 62.8 million tourists in 2017. Several sources have ranked New York the most photographed city in the world. Times Square, iconic as the world's "heart" and its "Crossroads", is the brightly illuminated hub of the Broadway Theater District, one of the world's busiest pedestrian intersections, and a major center of the world's entertainment industry. The names of many of the city's landmarks, skyscrapers, and parks are known around the world. Manhattan's real estate market is among the most expensive in the world. New York is home to the largest ethnic Chinese population outside of Asia, with multiple signature Chinatowns developing across the city. Providing continuous 24/7 service, the New York City Subway is the largest single-operator rapid transit system worldwide, with 472 rail stations. Over 120 colleges and universities are located in New York City, including Columbia University, New York University, and Rockefeller University, which have been ranked among the top universities in the world.  Anchored by Wall Street in the Financial District of Lower Manhattan, it has been called both the most economically powerful city and the leading financial center of the world, and the city is home to the world's two largest stock exchanges by total market capitalization, the New York Stock Exchange and NASDAQ.'''))
    
    
