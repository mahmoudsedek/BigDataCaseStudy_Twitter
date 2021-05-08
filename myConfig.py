import tweepy as tw

# APi Keys (+ secret) & Access Tokens (+ secret)
key = ['############################',
       '############################',
       '############################################',
       '############################################'
       ]
       
search_words = "#vaccinated" + "-filter:retweets"
search_words2 = "#covid_19" + "-filter:retweets"
search_words3 = "#COVIDSecondWave" + "-filter:retweets"
hashtag_demo = "#sedek_demo" + "-filter:retweets"

date_since = "2021-3-1"
date_until = "2021-4-28"
nrTweets = 7
broker_port = "sandbox-hdp.hortonworks.com:6667"
topic_name = "covid_vaccine"
parquet_directory = "hdfs://sandbox-hdp.hortonworks.com:8020/root/BigData_Mahmoud/covid_19"

# method to create API and check for credentials
def create_api():

   consumer_key = key[0]
   consumer_secret = key[1]
   access_token = key[2]
   access_token_secret = key[3]

   auth = tw.OAuthHandler(consumer_key, consumer_secret)
   auth.set_access_token(access_token, access_token_secret)
   api = tw.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

   try:
       api.verify_credentials()
       print("API created successfully ! \n")
   except:
       print("Check your credentials !!")
       exit()
   return api

