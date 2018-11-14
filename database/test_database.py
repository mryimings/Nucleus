import unittest
import sys
from os.path import dirname, abspath
d = dirname(dirname(abspath(__file__)))
sys.path.append(d)
from database.db_update_class import db

def count_rows(cursor):
    res = cursor.fetchone()
    return res[0]

# the test cases for database
class database_test_cases(unittest.TestCase):
    def setUp(self):
        self.db = db()
        self.sql_count_article = 'SELECT count(article_id) FROM HooliASE.articles'
        self.sql_count_question = 'SELECT count(question_id) FROM HooliASE.questions'
        self.sql_count_history = 'SELECT count(history_id) FROM HooliASE.history'

        self.sql_delete_article = 'DELETE from HooliASE.articles WHERE article_id=%s'
        self.sql_delete_question = 'DELETE from HooliASE.questions WHERE question_id=%s'
        self.sql_delete_history = 'DELETE from HooliASE.history WHERE history_id=%s'

    # add_article(title, content)
    def test_add_article(self):
        # count the original row number
        self.db.mycursor.execute(self.sql_count_article)
        ori_row = count_rows(self.db.mycursor)

        # add a new test record into articles table
        article_id = self.db.add_article('ASE', 'We all love ASE')

        # assert the success of insertion
        self.db.mycursor.execute(self.sql_count_article)
        new_row = count_rows(self.db.mycursor)
        self.assertEqual(new_row,ori_row+1)

        # delete the test record
        self.db.mycursor.execute(self.sql_delete_article, (article_id,))
        self.db.db.commit()

        # assert the deletion of test record
        self.db.mycursor.execute(self.sql_count_article)
        new_row = count_rows(self.db.mycursor)
        self.assertEqual(new_row,ori_row)

    # add_question(self, art_id, q_content):
    def test_add_question(self):
        # count the original row number
        self.db.mycursor.execute(self.sql_count_question)
        ori_row = count_rows(self.db.mycursor)

        # add a new test record into questions table
        question_id = self.db.add_question('1', 'what do we love?')

        # assert the success of insertion
        self.db.mycursor.execute(self.sql_count_question)
        new_row = count_rows(self.db.mycursor)
        self.assertEqual(new_row, ori_row + 1)

        # delete the test record
        self.db.mycursor.execute(self.sql_delete_question, (question_id,))
        self.db.db.commit()

        # assert the deletion of test record
        self.db.mycursor.execute(self.sql_count_question)
        new_row = count_rows(self.db.mycursor)
        self.assertEqual(new_row, ori_row)

    # add_history(self,u_id, q_id)
    def test_add_history(self):
        # count the original row number
        self.db.mycursor.execute(self.sql_count_history)
        ori_row = count_rows(self.db.mycursor)

        # add a new test record into history table
        history_id = self.db.add_history('1', '2')

        # assert the success of insertion
        self.db.mycursor.execute(self.sql_count_history)
        new_row = count_rows(self.db.mycursor)
        self.assertEqual(new_row, ori_row + 1)

        # delete the test record
        self.db.mycursor.execute(self.sql_delete_history, (history_id,))
        self.db.db.commit()

        # assert the deletion of test record
        self.db.mycursor.execute(self.sql_count_history)
        new_row = count_rows(self.db.mycursor)
        self.assertEqual(new_row, ori_row)

    # update(self,user_id, title, content, question)
    def test_update(self):
        self.db.mycursor.execute(self.sql_count_article)
        ori_row_article = count_rows(self.db.mycursor)
        self.db.mycursor.execute(self.sql_count_question)
        ori_row_question = count_rows(self.db.mycursor)
        self.db.mycursor.execute(self.sql_count_history)
        ori_row_history = count_rows(self.db.mycursor)

        flag_art, art_id, flag_q, q_id, h_id = \
            self.db.update(1,'Hooli', 'We are the team of Hooli','who are we?')

        self.db.mycursor.execute(self.sql_count_article)
        new_row_article = count_rows(self.db.mycursor)
        self.db.mycursor.execute(self.sql_count_question)
        new_row_question = count_rows(self.db.mycursor)
        self.db.mycursor.execute(self.sql_count_history)
        new_row_history = count_rows(self.db.mycursor)

        if flag_art:
            c = 0
        else:
            c = 1
        self.assertEqual(new_row_article,ori_row_article+c)
        self.assertEqual(new_row_history,ori_row_history+1)
        if flag_q:
            c = 0
        else:
            c = 1
        self.assertEqual(new_row_question,ori_row_question+c)

        if not flag_art:
            self.db.mycursor.execute(self.sql_delete_article, (art_id,))
            self.db.db.commit()
        if not flag_q:
            self.db.mycursor.execute(self.sql_delete_question, (q_id,))
            self.db.db.commit()
        self.db.mycursor.execute(self.sql_delete_history, (h_id,))
        self.db.db.commit()

        self.db.mycursor.execute(self.sql_count_article)
        new_row_article = count_rows(self.db.mycursor)
        self.assertEqual(new_row_article,ori_row_article)
        self.db.mycursor.execute(self.sql_count_question)
        new_row_question = count_rows(self.db.mycursor)
        self.assertEqual(new_row_question,ori_row_question)
        self.db.mycursor.execute(self.sql_count_history)
        new_row_history = count_rows(self.db.mycursor)
        self.assertEqual(new_row_history,ori_row_history)

    def close_db(self):
        self.db.db.close()

if __name__ == '__main__':
    unittest.main()
