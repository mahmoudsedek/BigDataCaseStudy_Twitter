# Sentiment analysis on streaming tweets using Spark DStream, Kafka, and Python
Regarding the situation all over the world I'll be focusing on COVID19.
The project aims at building a data platform streaming and analyzing of twitter data and the implementation will utilize different big data technologies as i'll describe below:

# Pipeline Description
After streaming this data and sending it to Kafka then start streaming it using Spark to (Process this tweets, Reply to user based on the sentiment_analysis AND writing parquet files of this tweets on HDFS to build a hive table on top of it, and last but not last using Power BI for visualiztion for delivering insights and data discovery.

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
