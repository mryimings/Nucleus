import mysql.connector

class db():
    def __init__(self):
        self.db = mysql.connector.connect(host='127.0.0.1', user='root',
                                     password='Li7953810', database='Holli')
        self.mycursor = self.db.cursor(buffered=True)

    def add_article(self,title, content):
        sql = 'INSERT INTO articles (article_title, article_content) VALUES (%s, %s)'
        val = (title, content)
        self.mycursor.execute(sql, val)
        self.db.commit()
        return self.mycursor.lastrowid


    def add_question(self,art_id, q_content):
        sql = 'INSERT INTO questions (article_id, question_content) VALUES (%s, %s)'
        val = (art_id, q_content)
        self.mycursor.execute(sql, val)
        self.db.commit()
        return self.mycursor.lastrowid


    def add_history(self,u_id, q_id):
        sql = 'INSERT INTO user_history (user_id, question_id) VALUES (%s, %s)'
        val = (u_id, q_id)
        self.mycursor.execute(sql, val)
        self.db.commit()
        return self.mycursor.lastrowid


    def update(self,user_id, title, content, question):
        try:
            self.mycursor.execute('SELECT article_id FROM articles WHERE article_title={}'.format(title))
            art_id = self.mycursor.fetchall()
            flag_art = True
        except mysql.connector.errors.ProgrammingError:
            flag_art = False
            art_id = self.add_article(title, content)

        try:
            self.mycursor.execute('SELECT question_id FROM questions WHERE question_content={} and article_id={}'.format(question,art_id))
            q_id = self.mycursor.fetchall()
            flag_q = True
        except mysql.connector.errors.ProgrammingError:
            flag_q = False
            q_id = self.add_question(art_id, question)
        h_id = self.add_history(user_id, q_id)
        return flag_art,art_id,flag_q,q_id,h_id
