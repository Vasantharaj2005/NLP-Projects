import tweepy
import json
import datetime as dt
import time
import os
import sys

'''
Updated to use Twitter API v2 with Tweepy 4.x.
Ensure you have a Bearer Token from Twitter Developer Portal.
'''

def load_api():
    ''' Load the Twitter API client using Bearer Token '''
    bearer_token = "Enter you bearer token"
    return tweepy.Client(bearer_token=bearer_token)

def tweet_search(client, query, max_tweets):
    ''' Search for recent tweets using Twitter API v2 '''
    tweets_data = []
    
    try:
        tweets = client.search_recent_tweets(query=query, max_results=min(max_tweets, 100), tweet_fields=["created_at", "id", "text"])
        
        if tweets.data:
            tweets_data = [tweet.data for tweet in tweets.data]
            print(f"Found {len(tweets_data)} tweets for query: {query}")
        else:
            print(f"No tweets found for query: {query}")

    except tweepy.TweepyException as e:
        print(f"Error fetching tweets: {e}")
        time.sleep(60)  # Wait before retrying

    return tweets_data

def write_tweets(tweets, filename):
    ''' Write tweets to a JSON file '''
    with open(filename, 'a') as f:
        for tweet in tweets:
            json.dump(tweet, f)
            f.write('\n')

def main():
    ''' Main function to search for tweets '''
    search_phrases = ['deepseek ai']
    max_tweets = 100  # Max tweets per search
    time_limit = 1.5  # Hours to run script

    client = load_api()  # Load API

    for search_phrase in search_phrases:
        print(f"Searching for tweets with: {search_phrase}")

        json_file = f"{search_phrase}.json"
        
        start = dt.datetime.now()
        end = start + dt.timedelta(hours=time_limit)

        while dt.datetime.now() < end:
            tweets = tweet_search(client, search_phrase, max_tweets)
            if tweets:
                write_tweets(tweets, json_file)
            time.sleep(60)  # Wait 1 min before next search

if __name__ == "__main__":
    main()
