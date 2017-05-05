import sys, os
sys.path.append("./app/")
from flask import Flask, request
from views import home
from views import api
from werkzeug.contrib.cache import SimpleCache

cache = SimpleCache()
app = Flask(__name__)
app.register_blueprint(home.app)
app.register_blueprint(api.app)

