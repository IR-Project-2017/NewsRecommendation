from flask import Blueprint, Flask, render_template, request
from elasticsearch import Elasticsearch
from db_communication import *
from cache import cache

es = Elasticsearch(index="")
app = Blueprint("home", __name__, url_prefix="")

@app.route("/")
def index():
    return render_template('home/index.html')

@app.route("/search")
def search():
    if request.method == "GET":
        q = request.args.get('q')
        username = request.args.get("username")
        if username is None:
            username = cache.get("username")
            user = get_user(username)
            gender = user["gender"]
            age = user["age"]
        else:
            gender = request.args.get("gender")
            age = request.args.get("age")
            user_data = {
                    "age": age,
                    "gender": gender
                    }
            add_user(username, user_data)

        set_cache(username)
        q_array = q.split(" ")
        query = construct_query(q_array)
        res = es.search(index="testindex", body=query)
        like_logs = cache.get(username + "_like_log")
        dislike_logs = cache.get(username + "_dislike_log")
    return render_template('home/search.html', articles=res["hits"]["hits"], like_logs=like_logs, dislike_logs=dislike_logs)

def set_cache(username):
    if cache.get("username") is None:
        cache.set("username", username)

def construct_query(q_array):
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
    return query
