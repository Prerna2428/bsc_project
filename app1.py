from flask import Flask,render_template,request,redirect,url_for,flash,session
from user import user_operation
from shop import shop_operation

import hashlib
from flask_mail import *
import random
from captcha.image import ImageCaptcha
from validate import myvalidate


app=Flask(__name__)
app.secret_key="gdfvdfrgrt45689"

#--------------------mail configuration-----------------------------------------------
app.config["MAIL_SERVER"]='smtp.office365.com'
app.config["MAIL_PORT"]='587'
app.config["MAIL_USERNAME"]='prernap28@outlook.com'
app.config["MAIL_PASSWORD"]='Prerna@123'
app.config["MAIL_USE_TLS"]=True
app.config["MAIL_USE_SSL"]=False
mail=Mail(app)


#-------------------------------------------------------------------------------------
@app.route('/')
def user_index():
    return render_template("user_dashboard.html")

@app.route('/user_signup')
def  user_signup():
    num=random.randrange(100000,999999)
    #create an image instance of the given size
    img= ImageCaptcha(width=280, height=90)

    #Image captcha text
    global captcha_text
    captcha_text=str(num)    #convert integer into string

    #write the image on the given file and save it
    img.write(captcha_text,'static/captcha/user_captcha.png')
    return render_template("user_signup.html")


@app.route('/user_signup_insert', methods=['GET','POST'])
def user_signup_insert():
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        address=request.form['address']
        pincode=request.form['pincode']
        city=request.form['city']
        password =request.form['password']
        mobile=request.form['mobile']

        #validation
        frm=[name,email,mobile,password]
        valid=myvalidate()
        v=valid.required(frm)
        if(v==False):
            flash("Field must be Filled!!!")
            return redirect(url_for("user_signup"))

         #captcha verification
        if captcha_text != request.form['captcha']:
            flash("Invalid Captcha")  
            return redirect(url_for("user_signup"))


        #---password encryption-------------
        pas=hashlib.md5(password.encode())
        password=pas.hexdigest()

        op=user_operation()  #object
        op.user_signup_insert(name,email,address,pincode,city,password,mobile)


        #--------email verification---------------
        global otp
        otp=random.randint(100000,999999)
        msg=Message('user verification',sender='prernap28@outlook.com', recipients=[email])
        msg.body="Hi "+ name +"\nYour email Otp is:" + str(otp)
        mail.send(msg)
        return render_template('email_verify.html',email=email)

        
@app.route('/email_verify', methods=['GET','POST'])
def email_verify():
    user_otp=request.form['otp']
    if otp==int(user_otp):
        flash("Your email verified.....")
        return redirect(url_for('user_login'))

    email=request.form['email']
    op=user_operation()
    op.user_delete(email)
    flash("Your email verification failed...")
    return redirect(url_for('user_signup'))

@app.route('/user_login')
def user_login():
    return render_template('user_login.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/review')
def review():
    return render_template('review.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/user_login_verify',methods=['GET','POST'])
def user_login_verify():
      if request.method=='POST':
            email=request.form['email']
            password=request.form['password']

            pas=hashlib.md5(password.encode())
            password=pas.hexdigest()

            op=user_operation()
            r=op.user_login_verify(email,password)
            if r==0:
              flash("Invalid user email and password!!!")
              return redirect(url_for('user_login'))
            else:
                return redirect(url_for('user_product_search'))
            


@app.route('/user_logout')
def user_logout():
        session.clear()
        flash("Logged out successfully!!!")
        return redirect(url_for('user_login'))


@app.route('/user_dashboard')
def user_dashboard():
            if 'user_email' in session:
                return render_template("user_dashboard.html")
            else:
                flash("You are not logged in.. please login now!!")
                return redirect(url_for('user_login'))



@app.route('/user_profile')
def user_profile():
        if 'user_email' in session:
            op = user_operation()
            row= op.user_profile()
            return render_template("user_profile.html",record=row)
        else:
           flash("You are not logged in.. please login now!!")
           return redirect(url_for('user_login'))

@app.route('/user_profile_edit',methods=['GET','POST'])
def user_profile_edit():
        if request.method=='POST':
                if 'user_email' in session:
                    name=request.form['name']
                    password=request.form['password']
                    op = user_operation()
                    op.user_profile_edit(name,password)
                    flash("your profile updated successfully!!")
                    return redirect(url_for('user_profile'))
                else:
                    flash("You are not logged in.. please login now!!")
                    return redirect(url_for('user_login'))


@app.route('/user_product_search')
def user_product_search():
    return render_template('user_product_search.html')


@app.route("/user_product_list", methods=['POST','GET'])
def user_product_list():
    if request.method=='POST':
        producttype=request.form["producttype"]
        #productname=request.form["productname"]
        op=user_operation()
        r=op.user_product_list(producttype)
        #r=op.user_product_list(productname)
        return render_template("user_product_search.html",record=r)



@app.route('/user_order',methods=['POST','GET'])
def user_order():
        if 'user_email' in session:
            if request.method=='GET':
                productid=request.args.get('productid')
                shop_email=request.args.get('shop_email')
                op = user_operation()
                op.user_order(productid,shop_email)
                flash("Product Ordered Successfully!!")
                return redirect(url_for('user_product_search'))
        else:

            flash("Kindly Login to Access this Page")
            return redirect(url_for('user_login'))

@app.route('/user_order_product_view')
def user_order_product_view():
    if 'user_email' in session:
        op=user_operation()
        r=op.user_order_product_view()
        flash("Product Ordered Successfully!!")
        return render_template("user_order_product_view.html",record=r)
    
    else:
        flash("Kindly Login to access this Page!!!")
        return redirect(url_for('user_login'))



#----------------------------------------------------------------------------------------------------------------#
#------------------------------------***SHOP MODULE****----------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------#


@app.route('/shop_signup')
def  shop_signup():
    
    return render_template("shop_signup.html")

@app.route('/shop_signup_insert', methods=['GET','POST'])
def shop_signup_insert():
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        address=request.form['address']
        pincode=request.form['pincode']
        password =request.form['password']
        mobile=request.form['mobile']
        #---password encryption-------------
        pas=hashlib.md5(password.encode())
        password=pas.hexdigest()

        op=shop_operation()  #object
        op.shop_signup_insert(name,email,address,pincode,password,mobile)


        #--------email verification---------------
        global otp
        otp=random.randint(100000,999999)
        msg=Message('user verification',sender='prernap28@outlook.com', recipients=[email])
        msg.body="Hi "+ name +"\nYour email Otp is:" + str(otp)
        mail.send(msg)
        return render_template('shop_email_verify.html',email=email)

        
@app.route('/shop_email_verify', methods=['GET','POST'])
def shop_email_verify():
    shop_otp=request.form['otp']
    if otp==int(shop_otp):
        flash("Your email verified.....")
        return redirect(url_for('shop_login'))

    email=request.form['email']
    op=shop_operation()
    op.shop_delete(email)
    flash("Your email verification failed...")
    return redirect(url_for('shop_signup'))

@app.route('/shop_login')
def shop_login():
    return render_template('shop_login.html')



@app.route('/shop_login_verify',methods=['GET','POST'])
def shop_login_verify():
      if request.method=='POST':
            email=request.form['email']
            password=request.form['password']

            pas=hashlib.md5(password.encode())
            password=pas.hexdigest()

            op=shop_operation()
            r=op.shop_login_verify(email,password)
            if r==0:
              flash("Invalid user email and password!!!")
              return redirect(url_for('shop_login'))
            else:
                return redirect(url_for('shop_dashboard'))
                

@app.route('/shop_logout')
def shop_logout():
        session.clear()
        flash("Logged out successfully!!!")
        return redirect(url_for('shop_login'))


@app.route('/shop_dashboard')
def shop_dashboard():
            if 'shop_email' in session:
                return render_template("shop_dashboard.html")
            else:
                flash("You are not logged in.. please login now!!")
                return redirect(url_for('shop_login'))


@app.route('/shop_profile')
def shop_profile():
        if 'shop_email' in session:
            op = shop_operation()
            row= op.shop_profile()
            return render_template("shop_profile.html",record=row)
        else:
           flash("You are not logged in.. please login now!!")
           return redirect(url_for('shop_login'))

@app.route('/shop_profile_edit',methods=['GET','POST'])
def shop_profile_edit():
        if request.method=='POST':
                if 'shop_email' in session:
                    name=request.form['name']
                    password=request.form['password']
                    op = shop_operation()
                    op.shop_profile_edit(name,password)
                    flash("your profile updated successfully!!")
                    return redirect(url_for('shop_profile'))
                else:
                    flash("You are not logged in.. please login now!!")
                    return redirect(url_for('shop_login'))


@app.route("/product")
def product():
    if 'shop_email' in session:
        return render_template("product.html")
    

    else:
        flash("Kindly  login to access this page")
        return redirect(url_for('shop_login'))


@app.route("/product_insert",methods=['POST','GET'])
def product_insert():
    if 'shop_email' in session:
        if request.method=='POST':
           
            productname=request.form['productname']
            producttype=request.form['producttype']
            price=request.form['price']
            expirydate=request.form['expirydate']
            #for photo
            photo_obj=request.files["photo"]
            photo= photo_obj.filename
            photo_obj.save("static/productimg/" + photo)
            description=request.form['description']
            op=shop_operation()
            op.product_insert(productname,producttype,price,expirydate,photo,description)
            flash("Your Product is Added Successfully!!!!!")
            return redirect(url_for('product'))

    else:
        flash("Kindly Login to Access this Page...")  
        return redirect(url_for('shop_login'))  


@app.route("/product_list")
def product_list():
    if 'shop_email' in session:
        op=shop_operation()
        r=op.product_list()
        return render_template("product_list.html",record=r)

    else:
        flash("Kindly Login to Access this Page...")  
        return redirect(url_for('shop_login'))   


@app.route("/product_delete",methods=['POST','GET'])
def product_delete():
    if 'shop_email' in session:
        productid=request.args.get('productid')
        op=shop_operation()
        op.product_delete(productid)
        flash("product is deleted successfully!!")
        return redirect(url_for('product_list'))
    

    else:
        flash("Kindly Login to Access this Page...")  
        return redirect(url_for('shop_login'))   

@app.route("/shop_product_view")
def shop_product_view():
    if 'email' in session:
        op=user_operation()
        r=op.shop_order_product_view()
        return render_template("shop_product_view.html",record=r)
    
    else:
        flash("Kindly Login to access this Page!!!")
        return redirect(url_for('user_login'))






if __name__=="__main__":
  app.run(debug=True)




