from app import app
from flask import render_template, redirect, url_for, flash, request, config,session,g,Markup,request
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.forms import RegistrationForm,LoginForm
from sqlalchemy import select,text,create_engine,DateTime,func,ForeignKey
from sqlalchemy.orm import  backref,relationship
from datetime import datetime,timedelta
import random



engine= create_engine('mysql://root:Hereniyah1999@localhost/jaribu',echo=False)

db=SQLAlchemy(app)
admin=Admin(app)

class Member(db.Model):
        NationalID = db.Column(db.Integer, primary_key=True)
        FirstName = db.Column(db.String(18),nullable=False)
        LastName = db.Column(db.String(18),nullable=False)	
        Email = db.Column(db.String(30),nullable=False,unique=True)
        PaymentCode = db.Column(db.String(10),nullable=False)
        PhoneNumber = db.Column(db.String(18),nullable=False,unique=True)
        Password = db.Column(db.Integer,nullable=False)
        """RegFeePaidStatus=db.Column(db.Boolean,default=False if RegDate="")"""
        RegDate = db.Column(DateTime(timezone=True),server_default=func.now())
        loan_id=db.Column(db.String(10),ForeignKey('loan.Id'))
        loans=relationship('Loan',backref=backref('member',uselist=False))
        #contributions=relationship('Contribution',backref=backref('member',uselist=False))
        dividends=relationship('Dividend',backref=backref('member',uselist=False))

class Loan(db.Model):
        Id = db.Column(db.String(10), primary_key=True)
        Principal = db.Column(db.Integer,nullable=False)
        Interest = db.Column(db.Integer,nullable=False)	
        InterestRate = db.Column(db.Float,nullable=False)
        DateBorrowed =db.Column(DateTime(timezone=True),server_default=func.now())
        LoanDuration= db.Column(db.DateTime)
        DateReturned= db.Column(db.DateTime,nullable=True)
        DefaultingStatus = db.Column(DateTime(timezone=True),server_default=func.now())
        DefaultingCharge = db.Column(DateTime(timezone=True),server_default=func.now())

"""class Contribution(db.Model):
        Id= db.Column(db.Integer, primary_key=True)
        ContribAmount= db.Column(db.Integer,default=0)
        PaymentCode = db.Column(db.String(10),nullable=False)	
        ContribDate= db.Column(DateTime(timezone=True),nullable=False,default="")
        ContribPaidStatus=db.Column(db.Boolean,default=False if ContribDate="")
        dividend_id=db.Column(db.Integer,ForeignKey('dividend.Id'),unique=True,nullable=False)
        dividends=relationship('Dividend',backref=backref('contribution',uselist=False))
        member_id=db.Column(db.Integer,ForeignKey('member.NationalID'),unique=True,nullable=False)
"""

class Dividend(db.Model):
        
        Id= db.Column(db.Integer, primary_key=True)
        DividendRatio= db.Column(db.Integer,nullable=False)
        DividendAmount = db.Column(db.Integer,nullable=False)
        PayoutDate=	db.Column(db.DateTime)
        member_id=db.Column(db.Integer,ForeignKey('member.NationalID'),unique=True,nullable=False)

    
db.create_all()

@app.route('/')
@app.route('/home')
def home():
    if 'loggedin' in session:
        return render_template('home.html', username=session['username'])


    else:
        return redirect(url_for('login'))

"""@app.route('/contributions')
def contributions():
    that_user=Member.query.filter_by(NationalID=session['id']).first()

    


    return render_template('contributions.html',title='Contributions',that_user=that_user)

@app.route("/check_contrib",methods=['POST','GET'])

def check_contrib():
    conn=engine.connect()
    now=datetime.now()
    pay_date=Contribution.query(ContribDate)
    next_contrib=pay_date+timedelta(days=30)
    notification_date=next_contrib - timedelta(days=2))
    latestBydate=notification_date + timedelta(days=4))
    if (pay_date is "" ) and (now >= latestBydate):
        conn.execute('al table contribution add column newContrib Integer')"""


@app.route('/loans',methods=['GET','POST'])
def loans():
    that_user=Member.query.filter_by(NationalID=session['id']).first()
    return render_template("loans.html",that_user=that_user)
@app.route('/register',methods=['GET','POST'])

    
def register():
    form = RegistrationForm()
    return render_template('register.html', title='Sign In',form=form)

@app.route('/editmember',methods=['GET','POST'])
def editmember():
    userinfo=Member.query.filter_by(NationalID=session['id']).first()
    return render_template('userDetails.html',title='User Details',userinfo=userinfo,username=session['username'])


@app.route('/userDetails')


def userDetails():
    if 'loggedin' in session: 
          userinfo=Member.query.all()
          db.session.commit()
          return render_template('userDetails.html',title='User Details',userinfo=userinfo,username=session['username'])
             
    return redirect(url_for('login'))
    
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
        conn=engine.connect()
        s=text("SELECT * FROM member WHERE NationalID = :id and Password = :password") 
        results=conn.execute(s,id=id,password=password)
        user=results.fetchone()

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
    conn=engine.connect()

    if form.validate_on_submit():
        password=form.password.data
        id=form.user_Id.data
        fname=form.firstName.data
        lname=form.lastName.data
        email=form.email.data
        number=form.phone_no.data
        t=text('SELECT * FROM member WHERE NationalID = :id')
        results=conn.execute(t,id=id)
        account=results.fetchone()
        if account:
            user=Member.query.filter_by(NationalID=id).first()
            flash(Markup(f'USER EXISTS ALREADY!!.PROCEED to LOGIN IF YOU ALREADY HAVE AN ACCOUNT.If you are not {user.LastName} ,Register an account <a href="/register" class="alert-link"> here</a>'))
            return redirect(url_for('login'))
        else:
            p=text("INSERT INTO  member(NationalID,FirstName,LastName,Email,PhoneNumber,Password) VALUES(:id, :fname, :lname, :email, :number, :password)")
            conn.execute(p,id=id,fname=fname,lname=lname,email=email,number=number,password=password)
            conn.close()
            flash(f'Your account has been created {form.firstName.data}!!.You are now able to login')
            return redirect(url_for('login'))
    return render_template('register.html', title='Sign In',form=form)
@app.route('/delete/<string:NationalID>', methods=['GET'])
def delete(NationalID):
    
    personTodelete=Member.query.filter_by(NationalID=NationalID).first()
    db.session.delete(personTodelete)
    db.session.commit()
    return redirect(url_for('userDetails'))
@app.route('/update', methods=['POST'])
def update():
    id_data=request.form['id']
    email=request.form['email']
    phonenumber=request.form['phonenumber']
    conn=engine.connect()
    u=text("UPDATE  member SET Email= :email,PhoneNumber= :phonenumber WHERE NationalID= :id_data")
    conn.execute(u,email=email,phonenumber=phonenumber,id_data=id_data)
    conn.close()

    return redirect(url_for('userDetails'))



admin.add_view(ModelView(Member,db.session))


if __name__ == "__main__":
        app.run(debug=True)
