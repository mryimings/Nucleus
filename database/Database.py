from datetime import datetime

import mysql.connector

from config import database_endpoint, database_pwd, database_user_name


class Database():
    def __init__(self):
        self.db = mysql.connector.connect(host=database_endpoint, user=database_user_name, password=database_pwd,
                                          database='HooliASE')
        self.mycursor = self.db.cursor(buffered=True)

    def add_user(self, user_name, user_pwd, user_email):
        sql = 'INSERT INTO users (name, password, email) VALUES (%s, %s, %s)'
        val = (user_name, user_pwd, user_email)
        if not (user_name == '' or user_pwd == '' or user_email == ''):
            self.mycursor.execute(sql, val)
            self.db.commit()
            return self.mycursor.lastrowid
        print('invalid input')
        return

    def add_article(self, title, content):
        sql = 'INSERT INTO articles (article_title, article_content) VALUES (%s, %s)'
        val = (title, content)
        if type(title) == str and type(content) == str and not (title == '' or content == '' or len(title) > 45):
            self.mycursor.execute(sql, val)
            self.db.commit()
            return self.mycursor.lastrowid
        print('invalid input')
        return

    def add_question(self, art_id, q_content, answer):
        sql = 'INSERT INTO questions (article_id, question_content, answer) VALUES (%s, %s, %s)'
        val = (art_id, q_content, answer)
        if art_id is not None and type(art_id) == int and type(q_content) == str and not (
                art_id < 0 or q_content == '' or len(q_content) > 45):
            self.mycursor.execute(sql, val)
            self.db.commit()
            return self.mycursor.lastrowid
        print('invalid input')
        return

    def add_history(self, u_id, q_id):
        sql = 'INSERT INTO history (user_id, question_id) VALUES (%s, %s)'
        val = (u_id, q_id)
        if u_id is not None and q_id is not None and type(u_id) == int and type(q_id) == int and not (
                u_id < 0 or q_id < 0):
            self.mycursor.execute(sql, val)
            self.db.commit()
            return self.mycursor.lastrowid
        print('negative input')
        return

    def update(self, user_id, title, content, question, answer):
        flag_art, flag_q = True, True
        type_cond = type(user_id) == int and type(title) == str and type(content) == str and type(question) == str
        if user_id == None:
            return
        if not type_cond or (title == '' or content == '' or question == '' or user_id < 0):
            return
        length_cond = len(title) < 45 and len(question) < 45
        if not length_cond:
            return
        # locate article id
        self.mycursor.execute("SELECT article_id FROM articles WHERE article_title='{}'".format(title))
        art_id = self.mycursor.fetchall()
        if not art_id:
            flag_art = False
            art_id = self.add_article(title, content)
        else:
            art_id = art_id[0][0]

        # locate question id
        self.mycursor.execute(
            "SELECT question_id FROM questions WHERE question_content='{}' and article_id={}".format(question, art_id))
        q_id = self.mycursor.fetchall()
        if not q_id:
            flag_q = False
            q_id = self.add_question(art_id, question, answer)
        else:
            q_id = q_id[0][0]

        # locate history id
        h_id = self.add_history(user_id, q_id)

        return flag_art, art_id, flag_q, q_id, h_id

    def get_id_by_name(self, username):
        sql = "SELECT user_id FROM users WHERE name = '{}'".format(username)
        self.mycursor.execute(sql)
        user_id = self.mycursor.fetchall()
        if len(user_id) > 0:
            return user_id[0][0]
        else:
            print("no username found, return -1")
            return -1

    def get_history_list(self, name, limit):
        user_id = self.get_id_by_name(name)
        history = []

        # in history table get question id
        self.mycursor.execute(
            'SELECT question_id FROM history WHERE user_id={} ORDER BY history_id DESC LIMIT {}'.format(user_id, limit))
        q_ids = self.mycursor.fetchall()
        if len(q_ids) == 0:
            print('no correspoding history found, return -1')
            return -1
        for q_id in q_ids:
            q_id = q_id[0]

            # in question table get question content and corresponding article id
            self.mycursor.execute(
                "SELECT question_content, article_id, answer FROM questions WHERE question_id={}".format(q_id))
            q_content, a_id, answer = self.mycursor.fetchall()[0]

            # in article table get article content and article title
            self.mycursor.execute(
                "SELECT article_content FROM articles WHERE article_id={}".format(a_id))
            a_content = self.mycursor.fetchall()[0]
            history.append((a_content, q_content, answer))
        return history

    def user_feedback(self, username, question, answer, satisfaction, expected=''):
        now = datetime.now()
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
        self.mycursor.execute("SELECT * from users WHERE name=%s",(username,))
        if(len(self.mycursor.fetchall())==0):
            return "No user found"
        if satisfaction < 0 or satisfaction > 10:
            return "Illegal satisfaction number"
        self.mycursor.execute(
            'insert into answer_feedback(username, question, returned_answer, satisfaction, expected_answer, time) '
            'values(%s, %s, %s, %s, %s, %s)', (username, question, answer, satisfaction, expected, formatted_date))
        self.db.commit()
        print("Feedback received, thank you!")
        return self.mycursor.lastrowid
