

from app import app,bcrypt
from flask_mysqldb import MySQL

from flask import render_template, redirect, url_for, flash, request, config
from app.forms import RegistrationForm,LoginForm

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='test'

mysql=MySQL(app)
@app.route('/')
@app.route('/home')
def home():
    return render_template('base.html')
@app.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()
    cur=mysql.connection.cursor()


    if form.validate_on_submit():
        hashed_pword=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        id=form.user_Id.data
        fname=form.firstName.data
        lname=form.lastName.data
        email=form.email.data
        number=form.phone_no.data
        pword=hashed_pword
        cur.execute("INSERT INTO  memberdetails(NationalID,FirstName,LastName,Email,PhoneNumber,Password)VALUES (%s,%s,%s,%s,%s,%s)",(id,fname,lname,email,number,pword))
        mysql.connection.commit()
        cur.close
        flash(f'Your account has been created {form.firstName.data}!!.You are now able to login')
        return redirect(url_for('login'))
    return render_template('register.html', title='Sign In',form=form)

@app.route('/userDetails')
def userDetails():
    cur=mysql.connection.cursor()
    results=cur.execute("SELECT * FROM memberdetails")
    if results > 0:
         userinfo=cur.fetchall()
    return render_template('userDetails.html',title='User Details',userinfo=userinfo)

@app.route('/login')
def login():
    form=LoginForm()
    return render_template('login.html',title='Login',form=form)



