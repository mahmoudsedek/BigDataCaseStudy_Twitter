# from collections import OrderedDict
import logging
import tweepy as tw
from myConfig import *
from time import sleep
from json import dumps
from kafka import KafkaProducer
import jsonpickle

# calling method from myConfig
api = create_api()

producer = KafkaProducer(bootstrap_servers=[broker_port], value_serializer=lambda x: dumps(x).encode('utf-8'))

records = {}
tweetsCheck = []

while True:
    # Collect tweets in a batch processing way (close to  NRT:near-real-time)
    tweets = tw.Cursor(api.search,
                       q=hashtag_demo,
                       lang="en",  # leave it to get all languages
                       since=date_since).items()  # if i wanna fetch only 5 #keep it items(5) ''',until=date_until''' # to specify specific duration

    for tweet in tweets:

        # check for duplicate tweets(the whole tweet: same user,content,date....) and add duplicates to a list        
        if tweet not in tweetsCheck:

            print("Streaming " + hashtag_demo.split('-')[0] + " tweets...\n")

            tweetContent = tweet.text
            tweetId = tweet.id_str
            print("Tweet: " + tweetContent + ">>>>> with tweet_id of: " + tweetId)
            userId = tweet.user.id_str
            userName = tweet.user.screen_name
            print("from user: " + userName + ">>>>> with id " + userId)
            userLocation = str(tweet.user.location)
            tweetDate = str(tweet.created_at)
            print("from loc. " + userLocation + ">>>>> on: " + tweetDate)
            source_App = str(tweet.source)
            print("source_App: " + source_App)

            followers_count = str(tweet.user.followers_count)
            print("followers_count: " + followers_count)
            following_count = str(tweet.user.friends_count)
            print("following_count: " + following_count)
            account_CreationDT = str(tweet.user.created_at)
            print("account_CreationDT on: " + account_CreationDT)
            favourites_count = str(tweet.user.favourites_count)
            print("favourites_count: " + favourites_count)
            # time_zone = str(tweet.user.time_zone)
            # print("time_zone: "+time_zone)
            verified = str(tweet.user.verified)
            print("verified ?: " + verified + "\n")
            # protected = str(tweet.user.protected)
            # print("protected ?: "+protected + "\n")

            # put your data in the order you wanna send them later with kafka producer
            records = {"userId": userId, "userName": userName, "tweetId": tweetId, "tweet": tweetContent,
                       "location": userLocation, "tweetDate": tweetDate, "source_App": source_App,
                       "followers_count": followers_count, "following_count": following_count,
                       "account_CreationDT": account_CreationDT, "favourites_count": favourites_count,
                       "verified": verified}

            # print("Get another related tweet...\n")

            # append those tweets in the list so if there's no more tweets in that HASHTAG our code won't send duplicate tweets to kafka-topic
            tweetsCheck.append(tweet)
            # print(tweetsCheck)
            # print(type(records))

            # sending tweets as it's in records dictionary [or a json object]
            finalRecord = jsonpickle.encode(records)
            producer.send(topic_name, value=finalRecord)
            sleep(2)  # sending each tweet to kafka-topic after 2 seconds

        else:
            print("No more tweets of topic: " + hashtag_demo.split('-')[0] + ", Keep listening...")
            sleep(60)  # if there's no more tweets about this #HASHTAG make the application wats for 1 minute before go and search for new data
        # consider it a pretty way to keep you script and twitter-api credentials safe from not being suspended :'D 

