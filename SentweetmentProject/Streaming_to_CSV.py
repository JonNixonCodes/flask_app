#!/usr/bin/env python3.4
"""
Initiate stream of Tweets to csv file
"""
import tweepy
import csv
import fcntl #for dealing with deadlock
import sys
import os

"""HACKY import custom modules from different directories"""
directories = os.getcwd().split('/')
#print(directories[-1])
if directories[-1] == 'flask_app':
    sys.path.append('SentweetmentProject/modules')
else:
    sys.path.append('modules')    
import twitterConnect_mod
import sentification_mod as sentification

"""global variables"""
fieldnames = ['tweet_id', 'author', 'text', 'date_created',
              'favourite_count', 'retweet_count', 'user_id',
              'user_followers_count', 'user_friends_count',
              'user_tweet_count', 'user_favourites_count',
              'user_lists_count', 'mention']
csvFile = None
csvWriter = None

class MyStreamListener(tweepy.StreamListener):
    """
    Instance of twitter stream, 
    containing all functions related to real-time processing 
    and batch storage of streaming data
    """
    BUF_SIZE = 100
    buf_count = 0
    buf = [] #buffer containing tweets

    
    def filter_tweet(self, tweet):
        """filter non-english tweets"""
        if tweet.lang != 'en':
            return False
        return True

    
    def flush_buf(self):
        """flush buffered tweets to csv file"""
        #lock file
        try:
            fcntl.flock(csvFile, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            print('Error: On obtaining lock, streaming continued')
            return -1 #exit with fail flag
        global csvFile, csvWriter
        csvWriter = csv.DictWriter(csvFile, fieldnames=fieldnames)
        for tweet in self.buf:
            csvWriter.writerow(tweet)
        #unlock file
        fcntl.flock(csvFile, fcntl.LOCK_UN)        
        self.buf = []
        self.buf_count = 0        
        print('\n\n########################################################')
        print('################## WROTE TO tweet.csv ##################')
        print('########################################################\n\n')
        

    def process_original_tweet(self, tweet, date_created):
        """append second-level tweets to buffer"""
        new = dict(
            tweet_id = tweet['id'],
            author = tweet['user']['screen_name'],
            text = tweet['text'],
            date_created = date_created,
            favourite_count = tweet['favorite_count'],
            retweet_count = tweet['retweet_count'],
            user_id = tweet['user']['id'],
            user_followers_count = tweet['user']['followers_count'],
            user_friends_count = tweet['user']['friends_count'],
            user_tweet_count = tweet['user']['statuses_count'],
            user_favourites_count = tweet['user']['favourites_count'],
            user_lists_count = tweet['user']['listed_count'],
            mention = False
        )
        #print(new)
        print('*', end='')
        self.buf.append(new)        
        self.buf_count += 1
        
    def process_tweet(self, tweet):
        """append immediate tweets to buffer"""        
        new = dict(
            tweet_id = tweet.id,
            author = tweet.author.name,
            text = tweet.text,
            date_created = tweet.created_at,
            favourite_count = tweet.favorite_count,
            retweet_count = tweet.retweet_count,
            user_id = tweet.user.id,
            user_followers_count = tweet.user.followers_count,
            user_friends_count = tweet.user.friends_count,
            user_tweet_count = tweet.user.statuses_count,
            user_favourites_count = tweet.user.favourites_count,
            user_lists_count = tweet.user.listed_count,
            mention = False
        )  
        if tweet.retweeted:
            #print(tweet.retweeted_status.status.text)
            self.process_original_tweet(tweet.retweeted_status, tweet.created_at)
        if hasattr(tweet, 'quoted_status'):
            #print(tweet.quoted_status)
            self.process_original_tweet(tweet.quoted_status, tweet.created_at)
        if tweet.in_reply_to_status_id is not None:
            new['mention'] = True
        print('*', end='')
        #print(new)
        self.buf.append(new)
        self.buf_count += 1
        
            
    def on_status(self, status):
        """for each tweet that is streamed, filter, process, flush buffer"""
        if self.filter_tweet(status) != True:
            return
        self.process_tweet(status)
        if self.buf_count > self.BUF_SIZE:
            #attempt to flush buffer
            self.flush_buf()

            
    def on_error(self, status_code):
        """on error code, disconnect"""
        print('Connection error: ', status_code)        
        if status_code == 420:
            #returning false on an on_data disconnects the stream
            return False
        else:
            return False

def main():
    query = 'python'
    query_id = 0
    """Get system arguments"""
    if (len(sys.argv)) > 0:
        query_id = sys.argv[1]
        query = sys.argv[2]
    print('query_id: {}'.format(query_id))        
    print('query: {}'.format(query))

    """open csv file"""
    global csvFile, csvWriter
    csvFile = open('{}_tweets.csv'.format(query_id), 'w', newline='')
    csvWriter = csv.DictWriter(csvFile, fieldnames=fieldnames)
    
    """connect to streaming api"""
    api = twitterConnect_mod.api
    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth=api.auth, listener=MyStreamListener())
    myStream.filter(track=[query])

    csvFile.close()

    
if __name__ == "__main__":
    main()
