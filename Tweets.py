import re

import tweepy as tweepy
import nltk
import pandas as pd
import string
from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.downloader.download('vader_lexicon')

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
        user = "TheNotoriousMMA"

        tweets = tweepy.Cursor(api.user_timeline, screen_name=user).items(10)

        #Raw tweets
        Rawtweets = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Raw_Tweets'])

        Rawtweets['Polarity'] = Rawtweets["Raw_Tweets"].apply(self.txtblob_polarity)
        print(Rawtweets)
        print(" ")

        tweets = tweepy.Cursor(api.user_timeline, screen_name=user).items(10)

        #Clean Tweets
        Cleantweets = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Clean_Tweet'])
        Cleantweets['Clean_Tweet'] = Cleantweets['Clean_Tweet'].apply(self.cleaning_tweets)

        Cleantweets['Polarity'] = Cleantweets['Clean_Tweet'].apply(self.txtblob_polarity)
        Cleantweets['Polarity_Vader'] = Cleantweets['Clean_Tweet'].apply(self.nltk_polarity)
       # print(Cleantweets)
        print(Cleantweets.to_string())

        return tweets


    def tokenize_tweets(self, tweets):

        tokenize_words = nltk.tokenize.word_tokenize(tweets)
        return tokenize_words


    def nltk_polarity(self, tweets):

        return SentimentIntensityAnalyzer().polarity_scores(tweets)

    def txtblob_polarity(self, tweets):

        return TextBlob(tweets).sentiment.polarity


    def remove_stopwords(self, tweets):
        stop_words = nltk.corpus.stopwords.words("english")
        # removing stop words
        tweeet = [sword for sword in tweets if sword not in stop_words]
        return tweeet

    def remove_special_char(self, tweets):
        # removing stop words
        tweeet = [schars for schars in tweets if schars not in string.punctuation]
        return tweeet

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
#test.remove_stopwords(test.tokenize_tweets("I am learning NLP"))
