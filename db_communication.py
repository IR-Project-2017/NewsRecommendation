from pymongo import MongoClient

#feedback is to be set to either "like" or "dislike"
def insert_user_feedback(user_id, title, date, feedback):
	if get_user(user_id).count() == 0:
		add_user(user_id, {})

	client = MongoClient()
	db = client.news_recommender
	collection = ""
	if feedback == "like":
		collection = db.likes
	elif feedback == "dislike":
		collection = db.dislikes
	else:
		print "Not supported feedback:", feedback
		return

	user_entries =collection.find({"user_id" : user_id})
	num_entries = user_entries.count()
	#If there are more than 5 entries, delete the oldest one
	#and insert the new one...
	if num_entries >= 5:
		print "Too many entries, deleting oldest one..."
		collection.delete_one({"_id" : user_entries[0]["_id"]})
	post = {
	"user_id" : user_id,
	"title" : title,
	"date" : date
	}
	collection.insert_one(post)
	print "Added entry..."

def get_users_likes(user_id):
	client = MongoClient()
	db = client.news_recommender
	collection = db.likes
	return collection.find({"user_id" : user_id}).sort("date")

def get_users_dislikes(user_id):
	client = MongoClient()
	db = client.news_recommender
	collection = db.dislikes
	return collection.find({"user_id" : user_id}).sort("date")

#user_data should be a dictionary, e.g. {"age" : 24, "location" : "Sweden"}
def add_user(user_id, user_data):
	client = MongoClient()
	db = client.news_recommender
	if 'profiles' not in db.collection_names():
		db.profiles.create_index([('user_id', pymongo.ASCENDING)], unique=True)

	collection = db.profiles

	user_data.update({"user_id" : user_id})
	
	try:
		collection.insert_one(user_data)
	except:
		print "Error while adding user, could be that there already exists a user with this user_id"

def get_user(user_id):
	client = MongoClient()
	db = client.news_recommender
	collection = db.profiles
	return collection.find({"user_id" : user_id})
