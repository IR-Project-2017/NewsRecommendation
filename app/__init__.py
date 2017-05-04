import sys, os
sys.path.append("./app/")
from flask import Flask, request
from views import home
from flask_mongoalchemy import MongoAlchemy

app = Flask(__name__)
app.register_blueprint(home.app)



