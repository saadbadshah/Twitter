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

        date_since = input("enter the date from which u want the tweets i.e (2021-01-1)")
        date_to = input("enter the date till which u want the tweets i.e (2021-01-1)")
        api = self.connect()
        user = input("Enter the Twitter you want tweets from: ")


        numoftweets = int(input("Enter the number of tweets you want: "))


        tweets = tweepy.Cursor(api.user_timeline,since=date_since,until=date_to,screen_name=user, ).items(numoftweets)



        #Raw tweets
        Rawtweets = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Raw_Tweets'])

        Rawtweets['Polarity_txtblob_Raw_Tweets'] = Rawtweets["Raw_Tweets"].apply(self.txtblob_polarity)
        Rawtweets['Polarity_vader'] = Rawtweets["Raw_Tweets"].apply(self.nltk_polarity)
        print(Rawtweets.to_string())
        print("Text Blob polarity Average: ")
        print(Rawtweets["Polarity_txtblob_Raw_Tweets"].astype(float).mean())
        print("Vader polarity Average: ")
        print( Rawtweets["Polarity_vader"].astype(float).mean())
        print(" ")

        tweets = tweepy.Cursor(api.user_timeline, screen_name=user).items(numoftweets)

        #Clean Tweets
        Cleantweets = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Clean_Tweet'])

        Cleantweets['Clean_Tweet'] = Cleantweets['Clean_Tweet'].apply(self.cleaning_tweets).apply(lambda x: self.tokenize_tweets(x.lower()))
        Cleantweets['Clean_Tweet'] = Cleantweets['Clean_Tweet'].apply(self.remove_stopwords).apply(self.remove_special_char)


        Cleantweets['Polarity'] = Cleantweets['Clean_Tweet'].apply(self.txtblob_polarity)
        Cleantweets['Polarity_Vader'] = Cleantweets['Clean_Tweet'].apply(self.nltk_polarity)

        print(Cleantweets.to_string())
        print("Text Blob polarity Average: ")
        print(Cleantweets["Polarity"].astype(float).mean())

        print("Vader polarity Average: ")
        print(Cleantweets["Polarity_Vader"].astype(float).mean())

        Polarity_Eval = Rawtweets[['Polarity_txtblob_Raw_Tweets']].copy()
        Polarity_Eval['Polarity_txtblob_Clean_Tweets'] = Cleantweets[['Polarity']].copy()


        Polarity_Eval['TxtBlob Polarity % change after Cleaning Tweets'] = (Polarity_Eval.Polarity_txtblob_Clean_Tweets - Polarity_Eval.Polarity_txtblob_Raw_Tweets) / abs(Polarity_Eval.Polarity_txtblob_Raw_Tweets) * 100
        print(Polarity_Eval.to_string())
        print(Polarity_Eval["TxtBlob Polarity % change after Cleaning Tweets"].astype(float).mean())

        Polarity_Eval_vader = Rawtweets[['Polarity_vader']].copy()
        Polarity_Eval_vader['Polarity_vader_Clean_Tweets'] = Cleantweets[['Polarity_Vader']].copy()

        Polarity_Eval_vader ['Vader Polarity % change after Cleaning Tweets'] = (Polarity_Eval_vader.Polarity_vader_Clean_Tweets - Polarity_Eval_vader.Polarity_vader  ) / abs(Polarity_Eval_vader.Polarity_vader) * 100
        print(Polarity_Eval_vader.to_string())
        print(Polarity_Eval_vader["Vader Polarity % change after Cleaning Tweets"].astype(float).mean())




        tweets = tweepy.Cursor(api.user_timeline, screen_name=user, ).items(numoftweets)

        # stock tweets
        StockTweets = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Stock_Tweets'])

        Stock = input("Please enter the Stock name or Ticker symbol that you might want to look at the tweets for (i.e NFLX, AMZN, Netflix or Amazon): ")
        StockTweets['Stock_Tweets'] = StockTweets[StockTweets['Stock_Tweets'].str.contains(pat=Stock, case=False)]
        StockTweets = StockTweets[StockTweets['Stock_Tweets'].notna()]

        StockTweets['Stock_Tweets'] = StockTweets['Stock_Tweets'].apply(self.cleaning_tweets).apply(
            lambda x: self.tokenize_tweets(x.lower()))
        StockTweets['Stock_Tweets'] = StockTweets['Stock_Tweets'].apply(self.remove_stopwords).apply(
            self.remove_special_char)

        StockTweets['Polarity'] = StockTweets['Stock_Tweets'].apply(self.txtblob_polarity)
        StockTweets['Polarity_Vader'] = StockTweets['Stock_Tweets'].apply(self.nltk_polarity)

        print(StockTweets.to_string())
        print("TxtBlob polarity Average: ")
        print(StockTweets["Polarity"].astype(float).mean())

        print("Vader polarity Average: ")
        print(StockTweets["Polarity_Vader"].astype(float).mean())



        stock_Ticker = input("Please enter the Stock Ticker Symbol for the data do be fetched(i.e NFLX): ")

        stockdata = StockData(stock_Ticker)


        return Cleantweets


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
        # removing stop words
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

