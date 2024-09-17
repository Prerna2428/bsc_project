import mysql.connector
from flask import session
from datetime import datetime

class user_operation:
    def connection(self):
        db=mysql.connector.connect(host="localhost",port="3306",user="root", password="root",database="rwc")
        return db

    def user_signup_insert(self,name,email,address,pincode,city,password,mobile):
        con=self.connection()
        sq="insert into user(name,email,address,pincode,city,password,mobile) values(%s,%s,%s,%s,%s,%s,%s)"
        record= [name,email,address,pincode,city,password,mobile]
        cursor=con.cursor()
        cursor.execute(sq,record)
        con.commit()
        cursor.close()
        con.close()
        return

    def user_delete(self,email):
        con=self.connection()
        sq="delete from user where email=%s"
        record=[email]
        cursor=con.cursor()
        cursor.execute(sq,record)
        con.commit()
        cursor.close()
        con.close()
        return

    def user_login_verify(self,email,password):
        con=self.connection()
        sq="select name,email from user where email=%s and password=%s"
        record=[email,password]
        cursor=con.cursor()
        cursor.execute(sq,record)
        row=cursor.fetchall()
        rc=cursor.rowcount
        cursor.close()
        con.close()
        if rc==0:
            return 0
        else:
            for r in row:
                session['user_name'] = r[0]
                session['user_email'] = r[1]
            return 1
    

    def user_profile(self):
        con=self.connection()
        sq="select name,email,password from user where email=%s"
        record=[session['user_email']]
        cursor=con.cursor()
        cursor.execute(sq,record)
        row=cursor.fetchall()
        cursor.close()
        con.close()
        return row

    def user_profile_edit(self,name,password):
        con=self.connection()
        sq="update user set name=%s, password=%s where email=%s"
        record = [name,password,session['user_email']]
        cursor=con.cursor()  
        cursor.execute(sq, record)
        con.commit()
        session['user_name']=name
        cursor.close()
        con.close()
        return   

    def user_product_list(self,producttype):
       con=self.connection()
       sq="select photo,productname,producttype,price,expirydate,description,productid,shop_email from product where producttype=%s"

       record=[producttype]
       cursor=con.cursor()
       cursor.execute(sq,record)
       row=cursor.fetchall()
       cursor.close()
       con.close()
       return row
       
       
    def user_order(self,productid,shop_email):
        con=self.connection()
        sq="insert into user_order(productid,user_email,shop_email,orderdate) values(%s,%s,%s,%s)"
        orderdate=datetime.now()
        record=[productid,session['user_email'],shop_email,orderdate]
        cursor=con.cursor()
        cursor.execute(sq,record)
        con.commit()
        cursor.close()
        con.close()
        return

    def user_order_product_view(self):
        con=self.connection()
        sq="select p.productid,productname,producttype,price,expirydate,photo from product p,user_order o where p.productid=o.productid and user_email=%s"
        record=[session['user_email']]
        cursor=con.cursor()
        cursor.execute(sq,record)
        row=cursor.fetchall()
        cursor.close()
        con.close()
        return row
        