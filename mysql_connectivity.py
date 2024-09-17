import mysql.connector
db=mysql.connector.connect(host="localhost",port="3306",user="root", password="root")


if db:
    print("Connection Successful")
else:
    print("connection fail")
