
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
        #self.import_tweets()
        self.raw_tweets()
        self.clean_tweets()
        self.search_tweets()

    def connect(self):
        #enter your twitter Api consumer key
        consumer_key = ''

        #enter the consumer secret key
        consumer_secret = ''
        
        #enter the access token
        access_token = ''

        #enter the access toke secret
        access_token_secret = ''

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True)
        return api

    def import_tweets(self):
        # Enter the use account you want the tweets imported from
        user = 'TheStreet'
        api = self.connect()
        tweets = tweepy.Cursor(api.user_timeline, screen_name=user).items(5)
        return tweets


    def makingdf(self, firstColum):

        try:
            tweets = self.import_tweets()
            StockTweets = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=[firstColum])
        except tweepy.TweepError:
            pass
        else:
            return StockTweets

    def raw_tweets(self):
        try:
            raw_tweets = self.makingdf('Raw_Tweets')
            raw_tweets['TxtBlob'] = raw_tweets['Raw_Tweets'].apply(self.txtblob_polarity)
            raw_tweets['Nltk'] = raw_tweets['Raw_Tweets'].apply(self.nltk_polarity)
        except TypeError:
            print("The twitter user account entered not found")
        else:
            print(raw_tweets.to_string())

    def clean_data(self,clean_tweets):
        try:
            clean_tweets['Clean_Tweets'] = clean_tweets['Clean_Tweets'].apply(self.cleaning_tweets).apply(lambda x: self.tokenize_tweets(x.lower()))
            clean_tweets['Clean_Tweets'] = clean_tweets['Clean_Tweets'].apply(self.remove_stopwords).apply(self.remove_special_char)

            clean_tweets['TxtBlob'] = clean_tweets['Clean_Tweets'].apply(self.txtblob_polarity)
            clean_tweets['Nltk'] = clean_tweets['Clean_Tweets'].apply(self.nltk_polarity)
        except TypeError:
            pass
        else:
            return clean_tweets

    def clean_tweets(self):
        try:
            clean_tweets = self.makingdf('Clean_Tweets')
            clean_tweets = self.clean_data(clean_tweets)
            print(clean_tweets.to_string())
        except AttributeError:
            pass

    def search_tweets(self):
        try:
            StockTweets = self.makingdf('Clean_Tweets')
            Stock = 'HNST'
            StockTweets['Clean_Tweets'] = StockTweets[StockTweets['Clean_Tweets'].str.contains(pat=Stock, case=False)]
            StockTweets = StockTweets[StockTweets['Clean_Tweets'].notna()]

            StockTweets = self.clean_data(StockTweets)
            print(StockTweets.to_string())

            stock_Ticker = input("Please enter the Stock Ticker Symbol for the data do be fetched(i.e NFLX): ")
            StockData(stock_Ticker)
        except TypeError:
            pass


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

