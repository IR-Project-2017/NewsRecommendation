from flask import Blueprint, Flask, render_template, request, jsonify
from elasticsearch import Elasticsearch
from db_communication import *
from datetime import datetime
from werkzeug.contrib.cache import SimpleCache
from cache import cache

es = Elasticsearch(index="")
app = Blueprint("api", __name__, url_prefix="/api")

@app.route("/like", methods=["POST"])
def like():
    username = cache.get("username")
    title = request.form["title"]
    article_id = request.form["id"]
    doc_type = request.form["doc_type"]
    print(doc_type)
    date = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    insert_user_feedback(username, title, date, "like", article_id)
    entries = get_users_likes(username)
    script = {"script":{"inline": "ctx._source.like +=1"}}
    es.update(index="testindex", doc_type=doc_type, body=script, id = article_id)
    logs = []
    for entry in entries:
        logs.append(entry["id"])
    cache.set(username + "_like_log", logs)
    return jsonify({})

@app.route("/dislike", methods=["POST"])
def dislike():
    username = cache.get("username")
    title = request.form["title"]
    id = request.form["id"]
    doc_type = request.form["doc_type"]
    date = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    insert_user_feedback(username, title, date, "dislike", id)
    entries = get_users_dislikes(username)
    script ={
            "script":{
                    "inline": "ctx._source.dislike += 1"
                }
            }
    es.update(index="testindex", doc_type=doc_type, id=id, body=script)
    logs = []
    for entry in entries:
        logs.append(entry["id"])
    cache.set(username + "_dislike_log", logs)
    return jsonify({})
