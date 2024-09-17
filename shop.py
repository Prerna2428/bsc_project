import mysql.connector
from flask import session

class shop_operation:
    def connection(self):
        db=mysql.connector.connect(host="localhost",port="3306",user="root", password="root",database="rwc")
        return db

    def shop_signup_insert(self,name,email,address,pincode,password,mobile):
        con=self.connection()
        sq="insert into shop(name,email,address,pincode,password,mobile) values(%s,%s,%s,%s,%s,%s)"
        record= [name,email,address,pincode,password,mobile]
        cursor=con.cursor()
        cursor.execute(sq,record)
        con.commit()
        cursor.close()
        con.close()
        return

    def shop_delete(self,email):
        con=self.connection()
        sq="delete from shop where email=%s"
        record=[email]
        cursor=con.cursor()
        cursor.execute(sq,record)
        con.commit()
        cursor.close()
        con.close()
        return

    def shop_login_verify(self,email,password):
        con=self.connection()
        sq="select name,email from shop where email=%s and password=%s"
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
                session['shop_name'] = r[0]
                session['shop_email'] = r[1]
            return 1
    

    def shop_profile(self):
        con=self.connection()
        sq="select name,email from shop where email=%s"
        record=[session['shop_email']]
        cursor=con.cursor()
        cursor.execute(sq,record)
        row=cursor.fetchall()
        cursor.close()
        con.close()
        return row

    def shop_profile_edit(self,name,password):
        con=self.connection()
        sq="update shop set name=%s, password=%s where email=%s"
        record = [name,password,session['shop_email']]
        cursor=con.cursor()  
        cursor.execute(sq, record)
        con.commit()
        cursor.close()
        con.close()
        return   

    
    
    def product_insert(self,productname,producttype,price,expirydate,photo,description):
        con=self.connection()
        sq="insert into product(shop_email,productname,producttype,price,expirydate,photo,description) values(%s,%s,%s,%s,%s,%s,%s)"
        record=[session['shop_email'],productname,producttype,price,expirydate,photo,description]
        cursor=con.cursor()
        cursor.execute(sq,record)
        con.commit()
        cursor.close()
        con.close()
        return

    def product_list(self):
        con=self.connection()
        sq="select productid,productname,producttype,price,expirydate,photo from product where shop_email=%s"
        record=[session['shop_email']]
        cursor=con.cursor()
        cursor.execute(sq,record)
        row=cursor.fetchall()
        cursor.close()
        con.close()
        return row
    
    def product_delete(self,productid):
        con=self.connection()
        sq="delete from product where productid=%s"
        record=[productid]
        cursor=con.cursor()
        cursor.execute(sq,record)
        con.commit()
        cursor.close()
        con.close()
        return

    def shop_ordered_product_view(self):
        con=self.connection()
        sq="select productid,productname,producttype,price,expirydate,photo from product where producttype=%s"
        record=[session['email']]
        cursor=con.cursor()
        cursor.execute(sq,record)
        row=cursor.fetchall()
        cursor.close()
        con.close()
        return row