import tweepy
import pandas as pd
import sys
import numpy as np
from preprocess_tweet import preprocess
from initialize_expertai_client import ExpertAiClient

client = ExpertAiClient()



"""authentication function"""
def twitter_api():
    try:
        consumer_key = "____________"
        consumer_secret = "____________"
        access_token = "____________________"
        access_secret = "_______________________"

    except KeyError:
        sys.stderr.write("TWITTER_* envirnoment variable not set\n")
        sys.exit(1)
    auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token,access_secret)
    api = tweepy.API(auth,wait_on_rate_limit= True)
    return api

def sentiment(text):
    """returns overall sentiment"""
    output = client.specific_resource_analysis(body = {"document":{"text": text}},
                                               params = {'language': 'en','resource': 'sentiment'})
    return output.sentiment.overall

def named_entity_extraction(text):
    """extract named entities"""
    output = client.specific_resource_analysis(body={"document": {"text": text}},
                                               params={'language': 'en', 'resource': 'entities'})
    return [entity.lemma for entity in output.entities]

def key_phrase_extraction(text):
    """extract key phrases"""
    output = client.specific_resource_analysis(body={"document": {"text": text}},
                                               params={'language': 'en', 'resource': 'relevants'})
    return [lemma.value for lemma in output.main_lemmas]

def tweet_user(username):
    """Extracting user information"""
    max_tweets = 1
    # Creation of query method using parameters
    tweets = tweepy.Cursor(api.user_timeline,id=username,tweet_mode = 'extended').items(max_tweets)
    tweets_list = [[preprocess(tweet.full_text), tweet.created_at, tweet.user.screen_name,] for tweet in tweets]
    # print(tweets_list)
    # Creation of dataframe from tweets_list
    # Did not include column names to simplify code

    tweets_df = pd.DataFrame(tweets_list)
    tweets_df.columns = ['tweets', 'time', 'screen_name',]
    tweets_df['tweet_sentiment'] = tweets_df['tweets'].apply(lambda x: sentiment(x))
    tweets_df['tweet_key_phrase'] = tweets_df['tweets'].apply(lambda x: key_phrase_extraction(x))
    tweets_df['tweet_NER'] = tweets_df['tweets'].apply(lambda x: named_entity_extraction(x))

    print(tweets_df.to_csv(f'{user}'))

if __name__ == '__main__':
    api = twitter_api()
    users = ['______________']
    for user in users:
         tweet_user(user)

