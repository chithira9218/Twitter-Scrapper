#importing modules
import snscrape.modules.twitter as sntwitter
import pandas as pd
import streamlit as st
import datetime
import pymongo
import time
 
#connecting  to mongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")  
#creating database
mydb = client["Twitter_Database"] 
#creating dataframe   
tweets_df = pd.DataFrame()
dfm = pd.DataFrame()
st.title(" Twitter Scrapper")
option = st.selectbox('Select an option:',('Keyword', 'Hashtag'))
word = st.text_input('Please enter a '+option, 'Example: Nestle')
start = st.date_input("Select the start date", datetime.date(2022, 1, 1),key='d1')
end = st.date_input("Select the end date", datetime.date(2023, 1, 1),key='d2')
tweet_c = st.slider('Select a Limit:', 0, 1000, 10)
#creating list to store scrapped data
tweets_list = []

# Scrape data
if word:
    if option=='Keyword':
        for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'{word} + since:{start} until:{end}').get_items()):
            if i>tweet_c:
                break
            tweets_list.append([ tweet.id, tweet.date,  tweet.content, tweet.lang, tweet.user.username, tweet.replyCount, tweet.retweetCount,tweet.likeCount, tweet.source, tweet.url ])
        tweets_df = pd.DataFrame(tweets_list, columns=['ID','Date','Content', 'Language', 'Username', 'ReplyCount', 'RetweetCount', 'LikeCount','Source', 'Url'])
    else:
        for i,tweet in enumerate(sntwitter.TwitterHashtagScraper(f'{word} + since:{start} until:{end}').get_items()):
            if i>tweet_c:
                break            
            tweets_list.append([ tweet.id, tweet.date,  tweet.content, tweet.lang, tweet.user.username, tweet.replyCount, tweet.retweetCount,tweet.likeCount, tweet.source, tweet.url ])
        tweets_df = pd.DataFrame(tweets_list, columns=['ID','Date','Content', 'Language', 'Username', 'ReplyCount', 'RetweetCount', 'LikeCount','Source', 'Url'])
else:
    st.warning(option,' cant be empty', icon="⚠️")

# DOWNLOAD AS CSV
@st.cache # IMPORTANT: Cache the conversion to prevent computation on every rerun
def convert_df(df):    
    return df.to_csv().encode('utf-8')

if not tweets_df.empty:
    csv = convert_df(tweets_df)
    st.download_button(label="Download CSV File",data=csv,file_name='Twitter_data.csv',mime='text/csv',)

    # DOWNLOAD AS JSON
    json_string = tweets_df.to_json(orient ='records')
    st.download_button(label="Download Json File",file_name="Twitter_data.json",mime="application/json",data=json_string,)

    # UPLOAD DATA TO DATABASE
    if st.button('Upload to Database'):
        coll=word
        coll=coll.replace(' ','_')+'_Tweets'
        mycoll=mydb[coll]
        dict=tweets_df.to_dict('records')
        if dict:
            mycoll.insert_many(dict) 
            ts = time.time()
            mycoll.update_many({}, {"$set": {"KeyWord_or_Hashtag": word+str(ts)}}, upsert=False, array_filters=None)
            st.success('Successfully uploaded to database', icon="✅")
        else:
            st.warning('Cant upload because there are no tweets', icon="⚠️")

    # display dataframe
    if st.button('View Dataframe'):
        st.write(tweets_df)

# display sidebar
with st.sidebar:   
    st.write('Uploaded Collections: ')
    for i in mydb.list_collection_names():
        mycollection=mydb[i]
        #st.write(i, mycollection.count_documents({}))        
        if st.button(i):            
            dfm = pd.DataFrame(list(mycollection.find())) 

# display collections
if not dfm.empty: 
    st.write(dfm) 





