import findspark

findspark.init()
import tweepy as tw
from myConfig import *
import time
from textblob import TextBlob
from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import json
from json import loads
import jsonpickle
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

# create spark configuration
conf = SparkConf()
conf.setAppName("TwitterStreamApp")

# create spark context with the above configuration
sc = SparkContext(conf=conf)
sc.setLogLevel("ERROR")
spark = SparkSession(sc)

# batch duration, here i process for each 2 seconds
ssc = StreamingContext(sc, 2)

KafkaStream = KafkaUtils.createDirectStream(ssc, topics=[topic_name], kafkaParams={"metadata.broker.list": broker_port})
KafkaStream.pprint()

# calling method from myAuthentication
api = create_api()

ts = time.time()  # for labeling reply instead of deleting it, don't forget to delete it :'D

# method to analysis and reply each tweet based on sentiment_analysis_popularity then return result (AKA reply/sentimentAnalysis) and pass down there to extractValues to put the value if (reply) in the returned newRow
def replyAndSentiment(tweetContent, tweetId, userName):
    sentimentAnalysis = TextBlob(tweetContent)
    # print(sentimentAnalysis.sentiment.polarity)
    if sentimentAnalysis.sentiment.polarity > 0:
        reply = 'Positive talk, thank you ' + userName + str(ts)
        result = 'Positive talk'
    elif sentimentAnalysis.sentiment.polarity == 0:
        reply = 'Well ' + userName + ' I think you need to explain a little bit' + str(ts)
        result = 'Neutral'
    else:
        reply = 'Okay, ' + userName + ' this sounds very bad' + str(ts)
        result = 'Negative'
    try:
        api.update_status(status=reply, in_reply_to_status_id=tweetId, auto_populate_reply_metadata=True)
        print("Replying to user: " + userName + " on tweet with ID: ", tweetId, " has been sent successfully!\n")
    except:
        print(
            "Already Replied on tweet id: " + tweetId)  # this to handle when trying to execute the method again because of the actions down there #you can put empty print if you don't want to bother yourself
    return result


# method responsible for decoding each row came from the rdd and take only needed values then pass newRow back to fetchData
def extractValues(row):
    # print("Processing tweets [inside extract]")
    row = row[1]  # value only of the coming dictionary
    Tweet = loads(row).encode('utf-8')  # decoding from Kafka Byte array
    finalTweet = jsonpickle.decode(Tweet)
    # values extracted from each row sent/fetched from Dstream (came from kafka-topic)
    userId = finalTweet["userId"]
    userName = finalTweet["userName"]
    tweetId = finalTweet["tweetId"]
    tweetContent = finalTweet["tweet"]
    userLocation = finalTweet["location"]
    tweetDate = finalTweet["tweetDate"]
    source_App = finalTweet["source_App"]
    followers_count = finalTweet["followers_count"]
    following_count = finalTweet["following_count"]
    account_CreationDT = finalTweet["account_CreationDT"]
    favourites_count = finalTweet["favourites_count"]
    verified = finalTweet["verified"]

    # calling replyAndSentiment to get the value of the reply (AKA sentiment_Analysis on each tweet)
    reply = replyAndSentiment(tweetContent, tweetId, userName)
    newRow = [userId, userName, tweetId, tweetContent, reply, userLocation, tweetDate, source_App, followers_count,
              following_count, account_CreationDT, favourites_count, verified]

    return newRow


# files checkpoint to prevent writing duplicate tweets in our parquet files
fileCheckList = []
try:
    print("Reading CASHED tweet IDs from fileCheckPoint...")
    fileCheckPoint = open("fileCheckPoint.txt", "r")
    for element in fileCheckPoint:
        element = element.split('\n')[0]
        fileCheckList.append(element)
except:
    print("CheckPoint File Not Exists!")


# method deals with the RDD and pass each rdd to extractValues method
def fetchData(rdd, spark):
    print("RDD is empty, Waiting for tweets...", rdd.isEmpty(), "\n")
    if (rdd.isEmpty() == False):
        print("Fetched some tweets, Start processing.....\n")
        rdd_list = rdd.map(extractValues)  # the returned rdd is a list, collect will return list of lists :'D

        # Schema to be used in our DataFrame which will later turned into parquet files
        twitterSchema = StructType([
            StructField("userId", StringType(), True),
            StructField("userName", StringType(), True),
            StructField("tweetId", StringType(), True),
            StructField("tweet", StringType(), True),
            StructField("reply", StringType(), True),
            StructField("userLocation", StringType(), True),
            StructField("tweetDate", StringType(), True),
            StructField("source_App", StringType(), True),
            StructField("followers_count", StringType(), True),
            StructField("following_count", StringType(), True),
            StructField("account_CreationDT", StringType(), True),
            StructField("favourites_count", StringType(), True),
            StructField("verified", StringType(), True)
        ])
        # print("identified the schema, after schema.. ")

        df = spark.createDataFrame(rdd_list, twitterSchema)

        # print("Creating DataFrame...") #with first action will go to extractValues first
        # df.show()  # show will do an action, making extractValues applies and the reply applies twice because next line also is an action,
        # go up there handle your replySentiment

        check = rdd_list.collect()  # another action will enforce the whole process
        check_var = check[0][2]
        # print(fileCheckList)

        if check_var not in fileCheckList:
            # print(check_var)
            # df.write.mode('append').parquet(parquet_directory)
            fileCheckList.append(check_var)
            print("Finished writing parquet file...\n")

            print("Adding tweetId to FileCheckPoint")
            fileCheckPoint = open("fileCheckPoint.txt", "w")
            for element in fileCheckList:
                fileCheckPoint.write(element + "\n")
            fileCheckPoint.close()
        else:
            print("Found Duplicate tweet_Id in CheckPointFile, IGNORE it !")
        # print(fileCheckList)


# first step to take the Dstream here and transform it to RDD
KafkaStream.foreachRDD(lambda rdd: fetchData(rdd, spark))

ssc.start()
ssc.awaitTermination()

