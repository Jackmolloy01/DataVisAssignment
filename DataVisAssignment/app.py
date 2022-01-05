from flask import Flask, render_template, request
from textblob import TextBlob
from twitter_auth import *
import tweepy as tp

from part1 import get_clean_tweets
from part2 import get_polarity, get_textblob_sentiment, get_accountAge

app = Flask(__name__)

@app.route('/', methods=['GET'])
def homepage():
    return render_template('index.html')

@app.route('/tweets', methods=['POST', 'GET'])
def display_graph():  # put application's code here

    query = request.form['query']
    query2 = request.form['query2']

    df = get_clean_tweets(query, "output")
    df2 = get_clean_tweets(query2, "output2")

# ========================== Vader sentiment ============================

    pos, neg, nue = get_polarity(df)
    pos2, neg2, nue2 = get_polarity(df2)

    labels = ['positive', 'negative', 'neutral']
    values = [pos, neg, nue]
    values2 = [pos2, neg2, nue2]

    data = zip(labels, values)
    data2 = zip(labels, values2)

    list1 = []

    for label, value in data:
        list1.append({'name': label, 'y': value, 'drilldown':label})

    list2 = []

    for label, value in data2:
        list2.append({'name': label, 'y': value, 'drilldown': label})

# ========================== Textblob sentiment ============================

    pos3, neg3, nue3 = get_textblob_sentiment(df)
    pos4, neg4, nue4 = get_textblob_sentiment(df2)

    values3 = [pos3, neg3, nue3]
    values4 = [pos4, neg4, nue4]

    data3 = zip(labels, values3)
    data4 = zip(labels, values4)

    list3 = []

    for label, value in data3:
        list3.append({'name': label, 'y': value, 'drilldown':label})

    list4 = []

    for label, value in data4:
        list4.append({'name': label, 'y': value, 'drilldown': label})

    return render_template('results.html', topic=query, topic2=query2, data=list1, data2=list2, data3=list3, data4=list4)


if __name__ == '__main__':
    app.run()
