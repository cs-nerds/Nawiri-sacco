from flask import Flask
from flask_bcrypt import Bcrypt
from config import Config

app=Flask(__name__)
app.config.from_object(Config)
bcrypt=Bcrypt(app)
from app import routes
