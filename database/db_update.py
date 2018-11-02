import mysql.connector

db = mysql.connector.connect(host='127.0.0.1', user='root',
                             password='', database='mydatabase')

print(db)

mycursor = db.cursor()
# mycursor.execute("CREATE DATABASE mydatabase") 1234567899999
# mycursor.execute("SHOW DATABASES")
# mycursor.execute("CREATE TABLE customers (name VARCHAR(255), address VARCHAR(255))")


# for x in mycursor:
#   print(x)

class User:
    def init(self, name, password, email):
        self.name = name
        self.password = password
        self.email = email


class Article:
    def init(self, title, content):
        self.title = title
        self.content = content


def add_article(title, content):
    sql = 'INSERT INTO articles (article_title, article_content) VALUES (%s, %s)'
    val = (title, content)
    mycursor.execute(sql, val)
    db.commit()
    return mycursor.lastrowid


def add_question(art_id, q_content):
    sql = 'INSERT INTO questions (article_id, question_content) VALUES (%s, %s)'
    val = (art_id, q_content)
    mycursor.execute(sql, val)
    db.commit()
    return mycursor.lastrowid


def add_history(u_id, q_id):
    sql = 'INSERT INTO user_history (user_id, question_id) VALUES (%s, %s)'
    val = (u_id, q_id)
    mycursor.execute(sql, val)
    db.commit()
    return mycursor.lastrowid


def update(user_id, title, content, question):
    mycursor.execute('SELECT article_id FROM articles WHERE article_title=title')
    art_id = mycursor.fetchall()
    if not art_id:
        art_id = add_article(title, content)
    q_id = add_question(art_id, question)
    h_id = add_history(user_id, q_id)
