# Sentiment analysis on streaming tweets using Spark DStream, Kafka, and Python
Regarding the situation all over the world I'll be focusing on COVID19.
The project aims at building a data platform streaming and analyzing of twitter data and the implementation will utilize different big data technologies as i'll describe below:

# Pipeline Description
    1.After streaming this data and sending it to Kafka.
    2.Start streaming it using Spark to:
      a-Process this tweets.
      b-Reply to user based on the sentiment_analysis.
      c-writing parquet files of this tweets on HDFS.
    3.Build a hive table on top of these parquet files.
    4.And last but not least using Power BI for visualiztion for delivering insights and data discovery.

# Setting up the Development Environment (those are main packages you can find rest of them inside the code):
  a)Create a twitter Developer Account Application to get an authentication keys to fetch data through their API.
  b)Synchronizes HDP datetime with UTC (Universal Time Coordination), which Sandbox runs on, it is needed to avoid running into authentication errors when connecting to the Twitter API, use: 
  >>> ntpdate -u time.google.com 
  OR 
  >>> sudo timedatectl set-timezone Africa/Cairo 
  >>> THEN >>> date -s "02 MAY 2021 13:40:00"
  
  b) HDP 2.6.5
  
  c) Creating virtual environemt (with these main packages):
   >>> python3.6 -m venv ./iti41 >>>
   >>> source iti41/bin/activate >>>
   >>> pip install --upgrade pip >>>
   >>> pip install confluent-kafka >>>
   >>> pip install pyspark==2.4.6 >>>
   >>> pip install tweepy >>>
   >>> pip install textblob >>>
 
   # Steps:
    1. myConfig.py
        a) Put you Tokens, Keys in the key dictionary.
        b) Edit the parquet_directory with wherever you want to save your parquet files.
        c) Change #HASHTAG ,date_since & date_until with whatever value you want.
        d) NOTE: you'll need to change the #HASHTAG value inside [ scrapper.py ] each time you fetch #HASHTAG tweets.

    2. scrapper.py
        a) NOTE: first run the scrapper.py to create the Kafka-topic (you can run it only for few seconds)  
        b) RUN: python scrapper.py
        c) You can remove whatever prints in the code, just put them to demonstrate how the data looks like to get you deeply inside the code.

    3. spark-Kafka.py
        a) Make sure to run this first then run scrapper.py (of course after creating the topic in step-2-a)
        a) RUN: spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8-assembly_2.11:2.4.6  --master local spark-Kafka.py

    4. HIVE table
    a) 1st table
    CREATE EXTERNAL TABLE if not exists twitter.covid_19 (userId string, userName string, tweetId string, tweet string, reply string, userLocation string,
    tweetDate string, source_app string, followers_count string, following_count string,account_creationdt string, favourites_count string, verified string,)
    stored as parquet LOCATION 'hdfs://sandbox-hdp.hortonworks.com:8020/root/BigData_Mahmoud/covid_19' 

    b) 2nd table
     CREATE EXTERNAL TABLE if not exists twitter.vaccine (userId string, userName string, tweetId string, tweet string, reply string, userLocation string,
    tweetDate string, source_app string, followers_count string, following_count string,account_creationdt string, favourites_count string, verified string,)
    stored as parquet LOCATION 'hdfs://sandbox-hdp.hortonworks.com:8020/root/BigData_Mahmoud/vaccine'
