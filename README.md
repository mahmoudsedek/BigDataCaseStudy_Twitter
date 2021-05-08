# Sentiment analysis on streaming tweets using Spark DStream, Kafka, and Python
The project aims at building a data platform for real time moderation and analytics of twitter data and the implementation will utilize different big data technologies as i'll describe below:

# Workflow
after streaming this data and sending it to Kafka then start streaming it using Spark to (Process this tweets, Reply to user based on the sentiment_analysis AND writing parquet files of this tweets on HDFS to build a hive table on top of it, and last but not last using Power BI for visualiztion for delivering insights and data discovery.

Architecture: stream data from Twitter, sending it to kafka then streaming it using Spark clean it, and apply a simple sentiment analysis model to detect the polarity of each tweet and reply to each tweet according if it's a negative or positive tweets, then I attempt to visualize the data using Power BI as a visualization tool connected to Hive table to answer business questions regarding the situation of COVID19 in India.
