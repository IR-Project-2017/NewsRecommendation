import praw
from elasticsearch import Elasticsearch
from datetime import datetime

es = Elasticsearch()

reddit = praw.Reddit(client_id='kiEkGfkxQ71Dpg',
                     client_secret='2wk6Gihtvtx3B8PyPJ8CLV9X23s',
                     user_agent='PrawScraper',
                     username='schoolstuff01',
                     password='kth123456')

top_posts = reddit.subreddit("worldnews").top(limit=1000)

doc = {
    "url": "url",
    "title": "title"
}

for post in top_posts:
    doc = {
        "url": post.url.encode('ascii', "ignore").decode("ascii"),
        "title": post.title.encode('ascii', "ignore").decode("ascii"),
        'timestamp': datetime.now()
    }
    res = es.index(index="testindex", doc_type='worldnews', id=post.id, body=doc)
    print("Indexed doc with ID: " + post.id)
