from flask import Blueprint, Flask, render_template, request
from elasticsearch import Elasticsearch
from app.models.profile import Profile

es = Elasticsearch(index="")
app = Blueprint("home", __name__, url_prefix="")

@app.route("/")
def index():
    return render_template('home/index.html')

@app.route("/search")
def search():
    if request.method == "GET":
        q = request.args.get('q')
        q_array = q.split(" ")
        condition = []
        for ele in q_array:
            condition.append({
                    "match": {
                        "title": ele
                            }
                    }
            )
        query = {"query":{
                    "bool": {
                        "should": condition
                        }
                    }
                }
        print(query)
        res = es.search(index="testindex", body=query)
    return render_template('home/search.html', articles=res["hits"]["hits"])
