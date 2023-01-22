#importing modules
import snscrape.modules.twitter as sntwitter
import pandas as pd
from IPython.display import display
from time import sleep
import pymongo
import streamlit as st
import datetime
import numpy as np



# Display the title
st.title("Twitter Scrapper")


#Form to display the Tweet
with st.form(key="form"):
        Username=st.text_input(label="Enter the Tweet")

    #Form to display the limit
        Number=st.slider("Enter the Limit",10,1000,500)
        st.write("Limit selected:",Number)

    # To display start date
        d = st.date_input(
        "Select StartDate",
        datetime.date(2019, 7, 6))
        st.write('start date:', d)
#   To display end date
        f = st.date_input(
        "Select End Date",
         datetime.date(2020, 8, 10))
        st.write('end date:', f)
        st.form_submit_button('Store into MongoDB')
        st.form_submit_button('Download CSV File')
        st.form_submit_button('Download Json File')
        st.form_submit_button('Submit')
        
#Creating a list to store the scrapped data
tweet_data=[]

Username=input("Enter the Tweet:")
Number=int(input("How many tweets do you want to scrape:"))

#Connecting with MongoDB
myclient = pymongo.MongoClient("mongodb://localhost:27017/")


#Creating Database
db = myclient.scrapped_data



#Scraping the Twitter data
for i, tweets in enumerate(sntwitter.TwitterSearchScraper('{}'.format(Username)).get_items()):
    if i>Number:
        break
    tweet_data.append([tweets.date,tweets.id,tweets.content,tweets.user.username,tweets.url,tweets.hashtags,tweets.replyCount,tweets.likeCount])

 #Store the data in a collection labeled with the Username
start_date = datetime.datetime(2023, 1, 1)
end_date = datetime.datetime(2023, 1, 20)
time_interval = end_date - start_date
collection=db[Username+str(time_interval)]



#Creating the dataframe
df = pd.DataFrame(tweet_data,columns=['Date','id','Tweets','username','url','Hashtag','Replycount','Likecount'])

#Display dataframe
display(df)



# Download the dataframe in CSV format
df.to_csv(f"{Username}_tweets.csv", index=False)


# Download the dataframe in JSON format
df.to_json(f"{Username}_tweets.json",orient='records', force_ascii=False, indent=4)
