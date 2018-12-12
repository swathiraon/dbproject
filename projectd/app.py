from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from flask_mysqldb import MySQL
from flask import json
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField
from passlib.hash import sha256_crypt
from functools import wraps
from flask_uploads import UploadSet, configure_uploads, IMAGES
import timeit
import datetime
from flask_mail import Mail, Message
import os
from werkzeug import generate_password_hash, check_password_hash
from wtforms.fields.html5 import EmailField





app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/image/product'
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)


mysql = MySQL()
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'swathi25_'
app.config['MYSQL_DB'] = 'uniformdb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Initialize the app for use with this MySQL class
mysql.init_app(app)

def getLoginDetails():
    
    cur = mysql.connection.cursor()
    if 'email' not in session:
        loggedIn = False
        firstName = ''
        noOfItems = 0
    else:
        loggedIn = True
        cur.execute("SELECT id, firstName FROM users WHERE email = %s", (session['email'], ))
        h=cur.fetchone()
        userId = h['id']
        firstName=h['firstName']
        print(userId)
        cur.execute("SELECT count(product_id) FROM cart WHERE uid = %s", (userId, ))
        noOfItems = cur.fetchone()['count(product_id)']
    cur.close()
    return (loggedIn, firstName, noOfItems)








# def is_logged_in(f):
#     @wraps(f)
#     def wrap(*args, **kwargs):
#         if 'logged_in' in session:
#             return f(*args, *kwargs)
#         else:
#             return redirect(url_for('login'))

#     return wrap


# def not_logged_in(f):
#     @wraps(f)
#     def wrap(*args, **kwargs):
#         if 'logged_in' in session:
#             return redirect(url_for('index'))
#         else:
#             return f(*args, *kwargs)

#     return wrap


# def is_admin_logged_in(f):
#     @wraps(f)
#     def wrap(*args, **kwargs):
#         if 'admin_logged_in' in session:
#             return f(*args, *kwargs)
#         else:
#             return redirect(url_for('admin_login'))

#     return wrap


# def not_admin_logged_in(f):
#     @wraps(f)
#     def wrap(*args, **kwargs):
#         if 'admin_logged_in' in session:
#             return redirect(url_for('admin'))
#         else:
#             return f(*args, *kwargs)

#     return wrap


# def wrappers(func, *args, **kwargs):
#     def wrapped():
#         return func(*args, **kwargs)

#     return wrapped


# def content_based_filtering(product_id):
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT * FROM products WHERE id=%s", (product_id,))  # getting id row
#     data = cur.fetchone()  # get row info
#     data_cat = data['category']  # get id category ex shirt
#     print('Showing result for Product Id: ' + product_id)
#     category_matched = cur.execute("SELECT * FROM products WHERE category=%s", (data_cat,))  # get all shirt category
#     print('Total product matched: ' + str(category_matched))
#     cat_product = cur.fetchall()  # get all row
#     cur.execute("SELECT * FROM product_level WHERE product_id=%s", (product_id,))  # id level info
#     id_level = cur.fetchone()
#     recommend_id = []
#     cate_level = ['v_shape', 'polo', 'clean_text', 'design', 'leather', 'color', 'formal', 'converse', 'loafer', 'hook',
#                   'chain']
#     for product_f in cat_product:
#         cur.execute("SELECT * FROM product_level WHERE product_id=%s", (product_f['id'],))
#         f_level = cur.fetchone()
#         match_score = 0
#         if f_level['product_id'] != int(product_id):
#             for cat_level in cate_level:
#                 if f_level[cat_level] == id_level[cat_level]:
#                     match_score += 1
#             if match_score == 11:
#                 recommend_id.append(f_level['product_id'])
#     print('Total recommendation found: ' + str(recommend_id))
#     if recommend_id:
#         cur = mysql.connection.cursor()
#         placeholders = ','.join((str(n) for n in recommend_id))
#         query = 'SELECT * FROM products WHERE id IN (%s)' % placeholders
#         cur.execute(query)
#         recommend_list = cur.fetchall()
#         return recommend_list, recommend_id, category_matched, product_id
#     else:
#         return ''


@app.route('/')
def home():
    # form = OrderForm(request.form)
    # # Create cursor
    # cur = mysql.connection.cursor()
    # # Get message
    # values = 'tshirt'
    # cur.execute("SELECT * FROM products WHERE category=%s ORDER BY RAND() LIMIT 4", (values,))
    # tshirt = cur.fetchall()
    # values = 'wallet'
    # cur.execute("SELECT * FROM products WHERE category=%s ORDER BY RAND() LIMIT 4", (values,))
    # wallet = cur.fetchall()
    # values = 'belt'
    # cur.execute("SELECT * FROM products WHERE category=%s ORDER BY RAND() LIMIT 4", (values,))
    # belt = cur.fetchall()
    # values = 'shoes'
    # cur.execute("SELECT * FROM products WHERE category=%s ORDER BY RAND() LIMIT 4", (values,))
    # shoes = cur.fetchall()
    # # Close Connection
    # cur.close()
    loggedIn=True
    if 'email' not in session:
        loggedIn=False
    return render_template('home.html',loggedIn=loggedIn)

@app.route('/uni/<string:gender>',methods=['GET', 'POST'])
def girls(gender):
    loggedIn=True
    if 'email' not in session:
        loggedIn=False
    if request.method=='POST':
        cur=mysql.connection.cursor()
        sid=request.form['school_id']
        print(sid)
        #gender='girls'

        cur.execute("SELECT * FROM UNIFORM u,CATEGORY c WHERE u.sid=%s and u.gender=%s and u.cate=c.id and c.id=%s",(sid,gender,1))
        res=cur.fetchall()
        print(res)
        cur.close()
        return render_template('list.html',posts=res)
    cur1=mysql.connection.cursor()
    cur1.execute("SELECT * from school")
    sch=cur1.fetchall()
    print(sch)
    cur1.close()
    return render_template('school.html',sch=sch,loggedIn=loggedIn)

# @app.route('/unib')
# def boys():
    

#     if request.method=='POST':
#         cur=mysql.connection.cursor()
#         sid=request.form['school_id']
#         gender='boys'
#         cur.execute("SELECT * FROM UNIFORM WHERE sid=? and gender=?",(sid,gender))
#         res=cur.fetchall()
#         return render_template('list.html',post=res)
#     cur=mysql.connection.cursor()
#     cur.execute("SELECT id,name from school")
#     sch=cur.fetchall()
#     cur.close()
#     return render_template('school.html',sch=sch)

@app.route('/unia',methods=['GET', 'POST'])
def access():

    loggedIn=True
    if 'email' not in session:
        loggedIn=False 
    if request.method=='POST':
        cur=mysql.connection.cursor()
        sid=request.form['school_id']
        print(sid)
        #gender='girls'
        
        cur.execute("SELECT * FROM UNIFORM u,CATEGORY c WHERE u.sid=%s and u.cate=c.id and c.id=%s ",(sid,2))
        res1=cur.fetchall()
        print(res1)
        cur.close()
        return render_template('list.html',posts=res1,loggedIn=loggedIn)


    cur=mysql.connection.cursor()
    cur.execute("SELECT id,name from school")
    sch=cur.fetchall()
    return render_template('school.html',sch=sch,loggedIn=loggedIn)

@app.route('/product/<int:pk>')
def product_details(pk):
    cur=mysql.connection.cursor()

    cur.execute("SELECT * FROM UNIFORM WHERE id=%s ",[pk])
    p=cur.fetchall()
    print(p)
    s=p[0]
    print(s)
    st=s['sid']
    print(st)
    cur.execute("SELECT name FROM school WHERE id=%s ",(st,))
    q=cur.fetchall()
    w=q[0]['name']
    cur.close()
    return render_template('details.html',p=p,q=w)


@app.route('/cart/<int:pid>')               

def add_cart(pid):
    cur=mysql.connection.cursor()
    cur.execute("SELECT * from cart where product_id=%s ",(pid,))
    print("cart/product_id")
    ww=cur.fetchall()
    print(cur.fetchall())
    
    if ww ==():
        print(ww)
        if 'email' not in session:
            return redirect(url_for('showSignin'))
        email = session.get('email')
        print(email)
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM users WHERE email = %s", (email, ))

        u = cur.fetchall()
        print(u)
        userId=u[0]['id']
        print(userId)
        cur.execute("INSERT into cart (uid,product_id,qty)values(%s,%s,%s)",(userId,pid,1))
        mysql.connection.commit()
        
        
        
    else:
        
        for w in ww:
            qt=w['qty']+1
            i=w['id']
             

            cur.execute("UPDATE cart SET qty = %s WHERE id=%s",(qt,i))



            mysql.connection.commit()

        
    cur=mysql.connection.cursor()
    cur.execute("SELECT * from cart c,uniform u where  c.product_id=u.id")
    aa=cur.fetchall()


    # Close Connection
    cur.close()
    return redirect(url_for('cart'))
@app.route('/cart')
def cart():
    if 'email' not in session:
        return redirect(url_for('showSignin'))
    loggedIn, firstName, noOfItems = getLoginDetails()
    email = session.get('email')
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT id FROM users WHERE email = %s", (email, ))

    u = cur.fetchall()
    userId=u[0]['id']
    print(userId)
    cur.execute("SELECT uniform.id, uniform.description, uniform.cost, uniform.img ,cart.qty FROM uniform, cart WHERE uniform.id = cart.product_id AND cart.uid = %s", (userId, ))
    products = cur.fetchall()
    print("products")
    print(products)
    totalPrice = 0
    for row in products:
        totalPrice += row['cost']*row['qty']
    return render_template("cart.html", products = products, totalPrice=totalPrice, loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems)

@app.route("/removeFromCart")
def removeFromCart():
    if 'email' not in session:
        return redirect(url_for('showSignin'))
    email = session.get('email')
    productId = int(request.args.get('productId'))
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT id FROM users WHERE email = %s", (email, ))
    userId = cur.fetchone()['id']
    try:
        cur.execute("DELETE FROM cart WHERE uid = %s AND product_id = %s", (userId, productId))
        mysql.connection.commit()
        msg = "removed successfully"
    except:
        mysql.connection.rollback()
        msg = "error occured"
    cur.close()
    return redirect(url_for('cart'))


@app.route('/showSignin')
def showSignin():
    cur1=mysql.connection.cursor()
    cur1.execute("SELECT * from school")
    sch=cur1.fetchall()
    print(sch)
    cur1.close()
    return render_template('signin.html',sch=sch)


@app.route('/validateLogin',methods=['POST'])
def validateLogin():
    try:
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']



    # connect to mysql

        cursor = mysql.connection.cursor()
        cursor.callproc('sp_validateLogin',(_email,))
        data = cursor.fetchall()
        print(data)



        if len(data) > 0:
            
            if check_password_hash(str(data[0]['password']),_password):
               # session['user'] = data[0]['id']
                session['email']=_email
                loggedIn = True
                session['logged_in'] = True
                print(session['email'])
                print(_email)
                return redirect(url_for('home'))
            else:
                return render_template('error.html',error = 'Wrong Email address or Password.')
        else:
            return render_template('error.html',error = 'Wrong Email address or Password.')

        cursor.close()
        
        print("wbfwehfbh")
    except Exception as e:
        return render_template('error.html',error = str(e))
        print(str(e))
    


@app.route('/userHome')
def userHome():
    if session.get('user'):
        return render_template('userHome.html')
    else:
        return render_template('error.html',error = 'Unauthorized Access')





@app.route('/logout')
def logout():
    session.pop('user',None)
    session.pop('email',None)
    return redirect('/')



@app.route('/signUp',methods=['POST','GET'])
def signUp():
    if request.method=='POST':
       
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']
        _lastName=request.form['inputlast']
        _sid=request.form['school_id']
        _mobile=request.form['inputPhone']
        _address=request.form['inputAddress']


        # validate the received values
        if _name and _email and _password:
            
            # All Good, let's call MySQL
            
            
            cursor = mysql.connection.cursor()
            _hashed_password = generate_password_hash(_password)
            args=(_name,_lastName,_email,_mobile,_address,_sid,_hashed_password)
            cursor.callproc('sp_createUser',args)
            data = cursor.fetchall()
            print(data)
            if len(data) is 0:

                mysql.connection.commit()

        #         if len(data) is 0:
        #             conn.commit()
                    
        #             return json.dumps({'message':'User created successfully !'})

        #         else:
        #             return json.dumps({'error':str(data[0])})
        #     else:
        #         return json.dumps({'html':'<span>Enter the required fields</span>'})

        # except Exception as e:
        #     return json.dumps({'error':str(e)})
        # finally:
            cursor.close() 
            
        return render_template('home.html')

    cur1=mysql.connection.cursor()
    cur1.execute("SELECT * from school")
    sch=cur1.fetchall()
    print(sch)
    cur1.close()
    return render_template('signup.html',sch=sch)

@app.route('/checkout')
def checkout():
    if 'email' not in session:
        return redirect(url_for('showSignin'))

    cur=mysql.connection.cursor()
    email=session.get('email')
    cur.execute("SELECT id,sid,address,mobile FROM users WHERE email = %s", (email, ))
    j=cur.fetchone()
    uid=j['id']
    sid=j['sid']
    address=j['address']
    mobile=j['mobile']
    tcost=float(request.args.get('totalCost'))
    cur.execute("INSERT into orders (uid,sid,oplace,mobile,total_cost)values(%s,%s,%s,%s,%s)",(uid,sid,address,mobile,tcost))
    mysql.connection.commit()
    cur.execute("SELECT * from cart where uid=%s",(uid,))
    cai=cur.fetchall()
    for ca in cai:
        cur.execute("INSERT into orddetails (product_id,qty)values(%s,%s)",(ca['product_id'],ca['qty']))

    cur.execute("UPDATE orddetails INNER JOIN uniform ON orddetails.product_id = uniform.id SET orddetails.cost=uniform.cost")
    mysql.connection.commit()

    cur.execute("DELETE  from cart where uid=%s",(uid,))
    mysql.connection.commit()

    cur.execute("SELECT o.id,o.total_cost,o.oplace,o.mobile from orders o,orddetails od where o.id=od.ord_id ")
    pp=cur.fetchone()
    print(pp)

    return render_template('orderdetails.html',pp=pp)
    



    




if __name__ == '__main__':
    app.static_folder = 'static'
    app.run(debug=True)