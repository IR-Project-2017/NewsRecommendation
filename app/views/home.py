from flask import Blueprint, Flask, render_template, request
from elasticsearch import Elasticsearch
from db_communication import *
from cache import cache
import pprint
import re

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
        else:
            user_data = {
                    }
            add_user(username, user_data)

        set_cache(username)
        q_array = q.split(" ")
        query = construct_query(q_array, username)
        res = es.search(index="testindex", body=query)
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(res["hits"]["hits"])
        like_logs = cache.get(username + "_like_log")
        dislike_logs = cache.get(username + "_dislike_log")
    return render_template('home/search.html', articles=res["hits"]["hits"], like_logs=like_logs, dislike_logs=dislike_logs, username=username)

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

    # disliked_orig_query = []
    # for disliked_doc in disliked_docs:
    #     resultwords  = [word for word in disliked_doc.split(" ") if word.lower() not in q_array]
    #     disliked_orig_query.append(' '.join(resultwords))
    # print(disliked_orig_query)

    if len(liked_docs) == 0:
        query = {
            "size": 50,
            "query":{
            "function_score":{
                "query": {
                    "more_like_this": {
                        "fields": ["title"],
                        "like": q_array,
                        "min_term_freq" : 1,
                        "max_query_terms" : 12,
                        "boost": 1.2

                    }
                },
                "field_value_factor":{
                    "field": "like",
                    "modifier": "log2p"
                }
            }

        }
        }

    else:
        query = {
            "size": 50,
            "query":{
            "function_score":{
            "query": {
            "dis_max":{
                "queries": [
                    {"more_like_this": {
                        "fields": ["title"],
                        "like": liked_docs,
                        "unlike": disliked_docs,
                        "min_term_freq" : 1,
                        "max_query_terms" : 12
                    }},
                    {"more_like_this": {
                        "fields": ["title"],
                        "like": q_array,
                        "unlike": disliked_docs,
                        "min_term_freq" : 1,
                        "max_query_terms" : 12,
                        "boost": 4.0
                    }}]
            }
        },
                "field_value_factor":{
                    "field": "like",
                    "modifier": "log2p"
                }
        }}

        }

    return query
