from flask import Flask
from flask_mongoalchemy import MongoAlchemy
from app import db

class Profile(db.Document):
    gender = db.BoolField() #0: woman, 1: man
    age = db.IntField()

