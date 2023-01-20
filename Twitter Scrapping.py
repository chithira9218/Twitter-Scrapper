
#Import_required_modules
import pandas as pd
import pymongo
import streamlit as st
import snscrape.modules.twitter as sntwitter
import datetime

# Create a text input for the Username
Username =input('Enter the Username:')
Limit=input('Enter the Limit')


# Connect to the database
client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
db = client.twitter_data


# Scrape tweets containing the hashtag
tweets = []
for tweet in sntwitter.TwitterSearchScraper('{}'.format(Username)).get_items():
    if len(tweets)== Limit:
        break
    else:
         tweets.append({'date': tweet.date, 'id': tweet.id, 'url': tweet.url,'tweet_content': tweet.content,'user': tweet.user.username, 'replyCount': tweet.replyCount, 'retweet_count': tweet.retweetCount,'language': tweet.lang, 'source': tweet.source, 'like_count': tweet.likeCount})


# Store the data in a collection labeled with the hashtag
start_date = datetime.datetime(2022, 12, 10)
end_date = datetime.datetime(2023, 1, 20)
time_interval = end_date - start_date
collection=db[Username+str(time_interval)]


 #Add a button to upload the data to the database
if st.button('Upload to database'):
      client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
      db = client.twitter_data
      collection=db[Username+str(time_interval)]
      st.success('Data uploaded')


# Converting collection to a dataframe
data = pd.DataFrame(list(collection.find()))

#To view dataframe
print(data)

# Download the CSV file
data.to_csv(f"{Username}_tweets.csv", index=False)

# Download the Json file
data.to_json(f"{Username}_tweets.json",orient='records', indent=4)
