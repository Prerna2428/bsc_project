import mysql.connector
mydb=mysql.connector.connect(host="localhost",port="3306",user="root",password="root",database="rwc")
mycursor=mydb.cursor()


sq="insert into user(name,email,mobile,password,pincode) values(%s,%s,%s,%s,%s)"

record=["prachi","prachi128@gmail.com","8232546398","166","7689"]
mycursor.execute(sq,record)

mydb.commit()