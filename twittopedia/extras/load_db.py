import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["twitter_analytics"]

mycol = mydb["hashtags"]

load_db = myclient["Twittopedia"]

load_col = load_db["hashtags"]

new_collection = load_db["analyzed"]

'''
for i in mycol.find():

	h = i["hashtag"]
	c = i["created_at"]

	for j in range(i["count"]):

		load_col.insert_one({"hashtag":h, "created_at":c})

		print(h)
'''

c = new_collection.find({"hashtag":"#KCON"})

print(c[0]["hashtag"])