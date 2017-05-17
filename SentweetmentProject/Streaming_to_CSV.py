#!/usr/bin/env python3.4
import tweepy
import csv
#dealing with deadlock
import fcntl
import sys
import os
directories = os.getcwd().split('/')
print(directories[-1])
if directories[-1] == 'flask_app':
    sys.path.append('SentweetmentProject/modules')
else:
    sys.path.append('modules')
    
import twitterConnect_mod
import sentification_mod as sentification


class MyStreamListener(tweepy.StreamListener):
    BUF_SIZE = 100
    buf_count = 0
    buf = []

    def filter_tweet(self, tweet):
        if tweet.lang != 'en':
            return False
        return True

    def flush_buf(self):
        #lock file
        try:
            fcntl.flock(csvFile, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            print('Error: On obtaining lock, streaming continued')
            return -1 #exit with fail flag
        fieldnames = ['author', 'text', 'date_created', 'favourited', 'retweeted']
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
        
    def process_tweet(self, tweet):
        new = dict(author = tweet.author.name,
             text = tweet.text,
             date_created = tweet.created_at,
             favourited = tweet.favorited,
             retweeted = tweet.retweeted)
        print('*', end='')
        """
        print('Date Created: ' + str(new['date_created']))
        print(new['text'])
        """
        self.buf.append(new)
    
    def on_status(self, status):
        if self.filter_tweet(status) != True:
            return
        self.process_tweet(status)
        self.buf_count += 1
        if self.buf_count > self.BUF_SIZE:
            #attempt to flush buffer
            self.flush_buf()
            
    #disconnect after receiving error 420
    def on_error(self, status_code):
        if status_code == 420:
            #returning false on an on_data disconnects the stream
            return False
        else:
            print('Connection error: ', status_code)
            return False

#Get system arguments
if (len(sys.argv)) > 0:
    query_id = sys.argv[1]
    query = sys.argv[2]
else:
    query_id = 0
    query = 'happy'

#query Twitter
api = twitterConnect_mod.api
#query = input('Enter your query: ')

# clear CSV file and write header
csvFile = open('{}_tweets.csv'.format(query_id), 'w', newline='')
fieldnames = ['author', 'text', 'date_created', 'favourited', 'retweeted']
csvWriter = csv.DictWriter(csvFile, fieldnames=fieldnames)
#csvWriter.writeheader()


myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=MyStreamListener())
myStream.filter(track=[query])

csvFile.close()
