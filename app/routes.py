 
from app import app
from flask_mysqldb import MySQL,MySQLdb

from flask import render_template, redirect, url_for, flash, request, config,session,g,Markup
from app.forms import RegistrationForm,LoginForm


app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='Hereniyah1999'
app.config['MYSQL_DB']='test'
app.config['MYSQL_CURSORCLASS']='DictCursor'

mysql=MySQL(app)
@app.route('/')
@app.route('/home')
def home():
    if 'loggedin' in session:
        return render_template('home.html', username=session['username'])


    else:
        return redirect(url_for('login'))
@app.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()
    return render_template('register.html', title='Sign In',form=form)

@app.route('/userDetails')
def userDetails():

          cur=mysql.connection.cursor()
          results=cur.execute("SELECT * FROM memberdetails")
          if results > 0:
             userinfo=cur.fetchall()
             return render_template('userDetails.html',title='User Details',userinfo=userinfo)

@app.route('/login', methods=['GET','POST'])
def login():
    form=LoginForm()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
    return render_template('login.html',title='Login',form=form)
@app.route('/checkUser', methods=['POST'])
def checkUser():
    form=LoginForm()
    if form.validate_on_submit():
        id=form.user_Id.data
        password=form.password.data
        cur=mysql.connection.cursor()
        cur.execute("SELECT * FROM memberdetails WHERE NationalID ='"+id+"' and Password ='"+password+"'")
        user=cur.fetchone()

        if user is None:
             return "Username or password is wrong"
        else:
            session['loggedin']= True
            session['id']= user['NationalID']
            session['username']= user['LastName']

            return redirect(url_for('home'))

    else:
        return render_template('login.html',title='Login',form=form)


@app.route('/logout')
def logout():
    session.pop('loggedin',None)
    session.pop('id',None)
    session.pop('username',None)
    return redirect(url_for('login'))
@app.route('/RegCheck', methods=['POST'])
def RegCheck():                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
    form = RegistrationForm()
    cur=mysql.connection.cursor()

    if form.validate_on_submit():
        password=form.password.data
        id=form.user_Id.data
        fname=form.firstName.data
        lname=form.lastName.data
        email=form.email.data
        number=form.phone_no.data
        cur.execute('SELECT * FROM memberdetails WHERE NationalID = %s', (id,))
        account=cur.fetchone()
        if account:
            flash(Markup(f'USER {form.firstName.data} EXISTS ALREADY!!.PROCEED to LOGIN.If you are not {form.firstName.data} ,Register an account <a href="/register" class="alert-link"> here</a>'))
            return redirect(url_for('register'))
        else:
            cur.execute("INSERT INTO  memberdetails(NationalID,FirstName,LastName,Email,PhoneNumber,Password)VALUES (%s,%s,%s,%s,%s,%s)",(id,fname,lname,email,number,password))
            mysql.connection.commit()
            cur.close
            flash(f'Your account has been created {form.firstName.data}!!.You are now able to login')
            return redirect(url_for('login'))
    return render_template('register.html', title='Sign In',form=form)
