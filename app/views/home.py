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
        query = construct_query(q_array, username)
        res = es.search(index="testindex", body=query)
        like_logs = cache.get(username + "_like_log")
        dislike_logs = cache.get(username + "_dislike_log")
    return render_template('home/search.html', articles=res["hits"]["hits"], like_logs=like_logs, dislike_logs=dislike_logs)

def set_cache(username):
    cache.set("username", username)

def construct_query(q_array, username):
    liked_docs = []
    for liked_doc in get_users_likes(username):
        liked_docs.append(liked_doc["title"])
        print(liked_doc)
    disliked_docs = []
    for disliked_doc in get_users_dislikes(username):
        disliked_docs.append(disliked_doc["title"])

    query = {"query": {
                "dis_max":{
                    "queries": [
                        {"more_like_this": {
                        "fields": ["title"],
                        "like": liked_docs,
                        "min_term_freq" : 1,
                        "max_query_terms" : 12
                    }},
                        {"more_like_this": {
                        "fields": ["title"],
                        "like": q_array,
                        "min_term_freq" : 1,
                        "max_query_terms" : 12,
                        "boost": 3
                    }}]
                }
            }
            }
    return query
