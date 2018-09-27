# File name : Streamer.py
# Technologies included : python, MongoDB
# Description : This file renders the live tweets from the twitter API and stores it in a MongoDB
# Use : Data Analytics
# Author: HemathKumar.R
# License : None


# Importing necessary Modules

from __future__ import absolute_import, print_function     # Basic Import (Not Necessary)
from tweepy.streaming import StreamListener     # Importing a Stream Listener from tweepy Module
from tweepy import OAuthHandler, Stream    # Importing needed classes from tweepy Module
import json, tweepy, pymongo     # Importing json for handling data via json, tweepy for confirm, pymongo for Mongo Database


# Important keys for Authentication, go to apps.twitter.com and create an app with your twitter developer id

# These keys will be kept in another file, and the values will be used by importing. It will be done after completing the project

consumer_key="XXXX Your Consumer Key XXXX"
consumer_secret="XXXX Your Consumer Secret Key XXXX"

access_token="XXXX Your Access Token XXXX"
access_token_secret="XXXX Your Access Token Secret Key XXXX"



# Establishing Database Connection with LocalHost, it will be configured with the specific Host on launching

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

# Creating a Database named 'twitter_analytics'

mydb = myclient["twitter_analytics"]

# Creating a new Collection named 'hashtags'

mycol = mydb["hashtags"]


# Creating a Listener class to handle the tweets from the stream, cute definition is below

""" A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
"""

class StdOutListener(StreamListener):

# Initializng class with certain values ( Constructor )

    def __init__(self):

        self.count = 0

        self.hashtag_list = []

# Overriding a previously defined method in tweepy module which is activated if the stream (API) is recieved without errors

    def on_data(self, data):

        self.count += 1

        jsonData = json.loads(data)
  
        try:

''' A little Algorithm (not a professional one, but it has an important role) which checks for the Hashtags and create a new collection
    in Database, if the same hastag is recieved, it will increment the existing argument named "count"
    which is the number of times that this specific hastag is used.
'''

            if "#" in jsonData["text"]:

                text_list = jsonData["text"].split()

                for elem in text_list:

                    if "#" in elem:

                        if elem not in self.hashtag_list:

                            det = {"hashtag":elem,"count":1,"created_at":jsonData["created_at"]}

                            mycol.insert_one(det)

                            self.hashtag_list.append(elem)

                        else:

                            c = mycol.find({"hashtag":elem})

                            cnt = c[0]["count"]

                            mycol.update_one({"hashtag":elem},{"$set":{"count":cnt+1}})

                            #print(elem)



        except KeyError:

            pass

        return True


# For now it just prints the HTTP error code if there is any error, later it will be changed to that it notifies the admin about the error.

    def on_error(self, status):

        print(status)

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)    # Authenticating the consumer keys
    auth.set_access_token(access_token, access_token_secret)    # Setting the access token after it's authentication

    stream = Stream(auth, l)

# sample() function streams all the live tweets
stream.sample()

# We may use filter(track=[]) function which takes list of strings as it's argument 'track', it will help us to filter out specific tweets from the given keyword.
