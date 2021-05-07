
import re

import tweepy as tweepy
import nltk
import matplotlib.pyplot as plt
import pandas as pd
import string
from textblob import TextBlob
from StockData import StockData
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.downloader.download('vader_lexicon')
nltk.download('stopwords')
nltk.download('punkt')
pd.set_option('use_inf_as_na', True)
class Get_Tweets():
    def __init__(self):
        self.import_tweets()
        self.raw_tweets()
        self.clean_tweets()
        self.search_tweets()

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
        user = 'TheStreet'
        api = self.connect()
        tweets = tweepy.Cursor(api.user_timeline, screen_name=user).items(5)

        return tweets


    def makingdf(self, firstColum):
        tweets = self.import_tweets()
        StockTweets = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=[firstColum])

        return StockTweets

    def raw_tweets(self):
        raw_tweets = self.makingdf('Raw_Tweets')
        raw_tweets['TxtBlob'] = raw_tweets['Raw_Tweets'].apply(self.txtblob_polarity)
        raw_tweets['Nltk'] = raw_tweets['Raw_Tweets'].apply(self.nltk_polarity)

        print(raw_tweets.to_string())

    def clean_data(self,clean_tweets):
        clean_tweets['Clean_Tweets'] = clean_tweets['Clean_Tweets'].apply(self.cleaning_tweets).apply(lambda x: self.tokenize_tweets(x.lower()))
        clean_tweets['Clean_Tweets'] = clean_tweets['Clean_Tweets'].apply(self.remove_stopwords).apply(self.remove_special_char)

        clean_tweets['TxtBlob'] = clean_tweets['Clean_Tweets'].apply(self.txtblob_polarity)
        clean_tweets['Nltk'] = clean_tweets['Clean_Tweets'].apply(self.nltk_polarity)

        return clean_tweets

    def clean_tweets(self):
        clean_tweets = self.makingdf('Clean_Tweets')
        clean_tweets = self.clean_data(clean_tweets)
        print(clean_tweets.to_string())

    def search_tweets(self):
        StockTweets = self.makingdf('Clean_Tweets')
        Stock = 'HNST'
        StockTweets['Clean_Tweets'] = StockTweets[StockTweets['Clean_Tweets'].str.contains(pat=Stock, case=False)]
        StockTweets = StockTweets[StockTweets['Clean_Tweets'].notna()]

        StockTweets = self.clean_data(StockTweets)
        print(StockTweets.to_string())

        stock_Ticker = input("Please enter the Stock Ticker Symbol for the data do be fetched(i.e NFLX): ")
        StockData(stock_Ticker)

    def nltk_polarity(self, tweets):
        polarity = SentimentIntensityAnalyzer().polarity_scores(tweets)
        return polarity['compound']

    def txtblob_polarity(self, tweets):
        return TextBlob(tweets).sentiment.polarity


    def tokenize_tweets(self, tweets):
        tokenize_words = nltk.tokenize.word_tokenize(tweets)
        return tokenize_words

    def remove_stopwords(self, tweets):
        stop_words = nltk.corpus.stopwords.words("english")
        # removing stop words

        tweeet = [sword for sword in tweets if sword not in stop_words]
        tweet = ' '.join(tweeet)
        return tweet

    def remove_special_char(self, tweets):

        tweeet = [schars for schars in tweets if schars not in string.punctuation]
        tweet = ''.join(tweeet)
        return tweet

#https://github.com/pjwebdev/Basic-Data-Science-Projects/blob/master/8-Twitter-Sentiment-Analysis/Tweeter%20Sentiment%20Analysis.ipynb the def contains regexes taken from this project
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

