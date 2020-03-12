

from app import app
from flask import render_template, redirect, url_for, flash, request, config
from app.forms import LoginForm



@app.route('/')
@app.route('/home')
def home():
    return render_template('base.html')
@app.route('/register',methods=['GET','POST'])
def register():
    form = LoginForm()

    if form.validate_on_submit():
        flash(f'Hello there {form.username.data}')
        return redirect(url_for('userDetails'))
    return render_template('register.html', title='Sign In',form=form)

@app.route('/userDetails')
def userDetails():
    return render_template('userDetails.html',title='User Details')
