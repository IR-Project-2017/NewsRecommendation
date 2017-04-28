from flask import Blueprint, Flask, render_template, request
app = Blueprint("home", __name__, url_prefix="")

@app.route("/")
def index():
    return render_template('home/index.html')

@app.route("/search")
def search():
    if request.method == "GET":
        query = request.args.get('q')
        print(query)
    return render_template('home/search.html')
