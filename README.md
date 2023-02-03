# Twitter-Scrapping

Twitter is a vast, open domain that suits best for scrapping. This project mainly aims to scrap Twitter data based on username or hashtag, then store the data as collection in MongoDB, after that creating adatframe and downloading it as CSV file and Json file.Scrapping Twitter data involves mainly based on id, Hashtag, Replycount, Likecount, Content, Url, Username, Content. The searching limit is set to be 1000. The basic workflow of the program is described below
      Importing required modules:snscrape
                                 pandas
                                 pymongo
                                 streamlit
                                 datetime
      
      Connecting to MongoDB
      Creating Database
      Creating a list to store the scrapped data
      Scraping the Twitter data based on the keyword or hashtag
      Appending it into the list
      Converting the list into dictionary
      Upload the data as collections in database
      Downoading as CSV File
      Downloading as Json File
      Developing a web app using streamlit to display the results(View dataframe, Upload into database, Downoad as csvfile, Download          as json file).    

      
      
