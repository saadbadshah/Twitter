import re

import tweepy as tweepy
import nltk
import pandas as pd

class Get_Tweets():
    def __init__(self):
        # self.connect()
        self.import_tweets()
        #self.connect()

    def connect(self):
        consumer_key = 'Ckf73BSAwbZuyjNQeDAVaxiRJ'
        consumer_secret = 'VGOblA0kCqCNvmz1gbeazA2T3kXlvgku7u0GU30BDWKNApbuia'
        access_token = '1309891053999321088-UsjY9LQRnaKVM2xTr2sWaWBBEQYv8E'
        access_token_secret = '0BnrxeKV788jZnm6lL0CZsMvLFJmIrF0ctOGlsOpG5MQq'

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True)
        return api

    def import_tweets(self):
        # Define the search term and the date_since date as variables
        search_words = "#wildfires" + " -filter:retweets"
        date_since = "2021-01-1"
        api = self.connect()
        user = "danawhite"
        tweets = tweepy.Cursor(api.user_timeline, screen_name=user).items(10)
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweet'])
        print(df)
        df['Tweet'] = df['Tweet'].apply(self.cleaning_tweets)
        print(df)
        return tweets

    def cleaning_tweets(self, txt):
        # Remove mentions
        txt = re.sub(r'@[A-Za-z0-9_]+', '', txt)
        # Remove hashtags
        txt = re.sub(r'#', '', txt)
        # Remove retweets:
        txt = re.sub(r'RT : ', '', txt)
        # Remove urls
        txt = re.sub(r'https?:\/\/[A-Za-z0-9\.\/]+', '', txt)
        return txt


test = Get_Tweets()

