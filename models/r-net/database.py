import mysql.connector

db = mysql.connector.connect(host='127.0.0.1', user='root',
    password='qweasdzxc', database="mydatabase")

print(db)

mycursor = db.cursor()
# mycursor.execute("CREATE DATABASE mydatabase")
# mycursor.execute("SHOW DATABASES")
mycursor.execute("CREATE TABLE customers (name VARCHAR(255), address VARCHAR(255))")
# for x in mycursor:
#   print(x)

def update():



# try:
#     with con.cursor() as cursor:
#         # Create a new record
#         sql = "select * from sys.sys_config"
#         print(cursor.execute(sql))
#
#     # connection is not autocommit by default. So you must commit to save
#     # your changes.
#     # connection.commit()
# finally:
#     con.close()