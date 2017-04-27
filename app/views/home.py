from flask import Blueprint, Flask, render_template
app = Blueprint("home", __name__, url_prefix="")

@app.route("/")
def index():
    return render_template('home/index.html')
