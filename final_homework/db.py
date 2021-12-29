import mysql.connector
connectiondb = mysql.connector.connect(host="localhost",user="root",passwd="Skills39",database="pygame")
cursordb = connectiondb.cursor()