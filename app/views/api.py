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
    print(username)
    title = request.form["title"]
    id = request.form["id"]
    date = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    insert_user_feedback(username, title, date, "like", id)
    entries = get_users_likes(username)
    logs = []
    for entry in entries:
        logs.append(entry["id"])
    cache.set(username + "_like_log", logs)
    return jsonify({})

@app.route("/dislike", methods=["POST"])
def dislike():
    username = cache.get("username")
    print(username)
    title = request.form["title"]
    id = request.form["id"]
    date = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    insert_user_feedback(username, title, date, "dislike", id)
    entries = get_users_dislikes(username)
    print("success2")
    logs = []
    for entry in entries:
        logs.append(entry["id"])
    cache.set(username + "_dislike_log", logs)
    return jsonify({})
