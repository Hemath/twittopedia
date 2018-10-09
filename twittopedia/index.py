# Importing necessary Modules #

from flask import Flask, render_template, request, jsonify, session, redirect, url_for

from operator import itemgetter

import pymongo, json, tweepy 

from tweepy.streaming import StreamListener

from tweepy import OAuthHandler, Stream

import variables

# Variables

Database_Host = variables.Database_Host

Database_Name = variables.Database_Name

Consumer_Key = variables.Consumer_Key

Consumer_Key_Secret = variables.Consumer_Key_Secret

Access_Token = variables.Access_Token

Access_Token_Secret = variables.Access_Token_Secret

Secret_Key = variables.Secret_Key

# Database Connection #

def connect_database(host,database,collection):

	myclient = pymongo.MongoClient(host)

	mydb = myclient[database]

	mycol = mydb[collection]

	return mycol

users_collection = connect_database(Database_Host, Database_Name, "users")

load_collection = connect_database(Database_Host, Database_Name, "hashtags")

new_collection = connect_database(Database_Host, Database_Name, "analyzed")

analyzed_collection = connect_database(Database_Host, Database_Name, "view")

drop_collection_1 = connect_database(Database_Host, Database_Name, "view")

drop_collection_2 = connect_database(Database_Host, Database_Name, "analyzed")

# Flask Configuration #

app = Flask(__name__)

app.secret_key = Secret_Key

#Routers

@app.route("/")
def index():

	return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():

	return render_template("check.html")

@app.route("/register_process", methods=["POST"])
def register_process():

	response = {"first_name":0, "last_name":0, "email":0, "password":0, "confirm_passowrd":0, "not_match":0, "status":"OK", "already":"NULL"}

	first_name = request.form["first_name"]

	last_name = request.form["last_name"]

	email = request.form["email"]

	password = request.form["password"]

	confirm_passowrd = request.form["confirm_password"]

	if first_name == "" or last_name == "" or email == "" or password == "" or confirm_passowrd == "" or password != confirm_passowrd:

		if first_name == "":

			response["first_name"] = 1

			response["status"] = "NULL"

		if last_name == "":

			response["last_name"] = 1

			response["status"] = "NULL"

		if email == "":

			response["email"] = 1

			response["status"] = "NULL"

		if password == "":

			response["password"] = 1

			response["status"] = "NULL"

		if confirm_passowrd == "":

			response["confirm_passowrd"] = 1

			response["status"] = "NULL"

		if password != confirm_passowrd:

			response["not_match"] = 1

			response["status"] = "NULL"

	else:

		values = {"First_Name":first_name, "Last_Name":last_name, "Email":email, "Password":password}

		for user in users_collection.find():

			if user["Email"] == email:

				response["already"] = "OK"

				response["status"] = "NULL"

				return json.dumps({"response":response})

		else:

			users_collection.insert_one(values)

	return json.dumps({"response":response})


@app.route("/login_process", methods=["POST"])
def login_process():

	response = {"login":"NULL"}

	email = request.form["email"]

	password = request.form["password"]

	for user in users_collection.find():

		if user["Email"] == email:

			got_email = 1

			if user["Password"] == password:

				got_password = 1

			else:

				got_password = 0

		else:

			got_email = 0


	if got_email and got_password:

		response["login"] = "success"

		session["email"] = email

	elif got_email and got_password==0:

		response["login"] = "wrong_password"

	elif got_email == 0:

		response["login"] = "no_user"

	return json.dumps({"response":response})

	#return redirect(url_for("dashboard"))

@app.route("/dashboard")
def dashboard():

	return render_template("dashboard.html")

@app.route("/view", methods=["GET"])
def view():

	hashtags_list = []

	count_list = []

	for i in analyzed_collection.find():

		hashtags_list.append(i["hashtag"])

		count_list.append(i["count"])

	return json.dumps({"hashtags_list":hashtags_list, "count_list":count_list})

@app.route("/analyze", methods=["GET"])
def analyze():

	print("Analyzing....")

	drop_collection_2.drop()

	hashtag_list = []

	for j in load_collection.find():

		if j["hashtag"] in hashtag_list:

			c = new_collection.find({"hashtag":j["hashtag"]})

			cnt = c[0]["count"]

			new_collection.update_one({"hashtag":j["hashtag"]},{"$set":{"count":cnt+1}})

		else:

			new_collection.insert_one({"hashtag":j["hashtag"], "count":1, "created_at":j["created_at"]})

			hashtag_list.append(j["hashtag"])

	print("Analyzing Finished....")

	return json.dumps({"response":"OK"})

@app.route("/update")
def update():

	print("Updating....")

	data_list = []

	for i in new_collection.find({"count":{"$gt":10}}):

		data_list.append([i["hashtag"],i["count"]])

		data_list.sort(key=lambda x:int(x[1]),reverse=True)

	data_list = data_list[:10]

	drop_collection_1.drop()

	for j in data_list:

		analyzed_collection.insert_one({"hashtag":j[0], "count":j[1]})

	print("done...")

	print("Updating Finished....")

	return json.dumps({"response":"OK"})

@app.route("/fetch", methods=["POST"])
def fetch():

	print("Fetching....")

	cnt = request.form["count"]

	print(cnt)

	class Fetcher(StreamListener):

		def __init__(self,cnt):

			self.count = int(cnt)

			print(self.count)

		def on_data(self, data):

			jsonData = json.loads(data)

			try:

				if "#" in jsonData["text"]:

					text_list = jsonData["text"].split()

					for elem in text_list:

						if "#" in elem:

							self.count -= 1

							det = {"hashtag":elem,"count":1,"created_at":jsonData["created_at"]}

							load_collection.insert_one(det)

			except KeyError:

				pass

			if self.count == 0:

				return False

			return True

		def on_error(self, status):

			print(status)
		
	l = Fetcher(cnt)

	auth = OAuthHandler(Consumer_Key, Consumer_Key_Secret)
	auth.set_access_token(Access_Token, Access_Token_Secret)
	stream = Stream(auth, l)
	#stream.filter(track=['cricket'])
	stream.sample()

	print("Fetching Finished....")

	return json.dumps({"response":"OK"})

# Checking for the Main #

if __name__ == '__main__':

	app.run(debug=True)