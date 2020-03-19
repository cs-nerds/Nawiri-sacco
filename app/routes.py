

from app import app
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
        cur.execute("INSERT INTO  memberdetails(NationalID,FirstName,LastName,Email,PhoneNumber,Password)VALUES (%s,%s,%s,%s,%s,%s)",(form.user_Id.data,form.firstName.data,form.lastName.data,form.email.data,form.phone_no.data,form.password.data))
        mysql.connection.commit()
        cur.close
        flash(f'Hello there {form.firstName.data}')
        return redirect(url_for('userDetails'))
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



