from flask import Flask, render_template, request
from textblob import TextBlob

from twitter_auth import *
import tweepy as tp
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
from datetime import datetime

app = Flask(__name__)

def clean_tweet(input):
    return re.sub('[^A-Za-z0-9 ]+','', input)

@app.route('/tweets', methods=['POST', 'GET'])
def get_clean_tweets(queryInput, outputName):
    auth = tp.OAuthHandler(API_KEY,API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    api = tp.API(auth)

    tweets = {}
    if request.method == 'POST':

        vdr = SentimentIntensityAnalyzer()
        tweets_from_api = api.search_tweets(queryInput,count=100)

        id = 0

        for tweet in tweets_from_api:
            tweets[id] = {
                'id':id,
                'username':tweet.user.name,
                'text': clean_tweet(tweet.text),
                'sentiment': vdr.polarity_scores(tweet.text)['compound'],
                'textblob': TextBlob(tweet.text).sentiment.polarity,
                'accountAge': datetime.now().year-tweet.user.created_at.year
            }
            id+=1

        df = pd.DataFrame.from_dict(tweets, orient='index')

        df.set_index('id', inplace=True)

        df.to_csv(outputName+'.csv')

    return df


if __name__ == '__main__':
    get_clean_tweets()