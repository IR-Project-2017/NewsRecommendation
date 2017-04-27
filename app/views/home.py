from flask import Blueprint, Flask

app = Blueprint("home", __name__, url_prefix="")

@app.route("/")
def index():
    print "hello world"
    return "hello"
