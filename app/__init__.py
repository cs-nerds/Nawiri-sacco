from flask import Flask

from config import Config


app=Flask(__name__)
app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:Hereniyah1999@localhost/jaribu'

from app import routes
