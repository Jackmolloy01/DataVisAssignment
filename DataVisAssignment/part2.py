import pandas as pd
from matplotlib import pyplot as plt
from textblob import TextBlob


def get_polarity(tweets):
    return (tweets['sentiment']> .25).sum(), (tweets['sentiment']< -0.25).sum(), (tweets['sentiment'].between(-0.25, .25)).sum()

def get_textblob_sentiment(tweets):
    return (tweets['textblob'] >= .25).sum(), (tweets['textblob'] <= -0.25).sum(), (tweets['textblob'].between(-0.25, .25)).sum()

def get_accountAge(tweets):
    return (tweets['accountAge'] <= 2010).sum(), (tweets['accountAge'] <= 2020).sum(), (tweets['accountAge'].between(2010, 2020)).sum()



