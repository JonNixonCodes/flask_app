#!/usr/bin/env python3.4
"""
Process tweets from file in batches
Output prevalence, sentiment, influence, polarity data to file for serving
"""
import csv
import datetime
import time
import fcntl #dealing with deadlock
import sys
import os
import nltk
from nltk.tokenize import word_tokenize, RegexpTokenizer, TweetTokenizer, WhitespaceTokenizer
import pickle
import emoji
from emoji import UNICODE_EMOJI, EMOJI_UNICODE

"""HACKY import custom modules from different directories"""
directories = os.getcwd().split('/')
if directories[-1] == 'flask_app':
    sys.path.append('SentweetmentProject/modules')
else:
    sys.path.append('modules')
import sentification_mod as sentification
import subjectification_mod as subjectification
import intensification_mod as intensification


"""Hacky solution to running script from different directory"""
preDir = ''
directories = os.getcwd().split('/')
if directories[-1] == 'flask_app':
    preDir = 'SentweetmentProject/'
f = open(preDir + 'modules/jar_of_pickles/emoji_unicode.pickle', 'rb')
emoji_unicode = pickle.load(f)
f.close()
f = open(preDir + 'modules/jar_of_pickles/happy_emoji_unicode.pickle', 'rb')
happy_emoji_unicode = pickle.load(f)
f.close()
f = open(preDir + 'modules/jar_of_pickles/neutral_emoji_unicode.pickle', 'rb')
neutral_emoji_unicode = pickle.load(f)
f.close()
f = open(preDir + 'modules/jar_of_pickles/sad_emoji_unicode.pickle', 'rb')
sad_emoji_unicode = pickle.load(f)
f.close()


def ProcessTweet(tweet, sentifier, subjectifier):
    """Process individual tweets and return metrics"""
    text = tweet['text']
    demoji_text, sentiment = FindEmoji(text)
    if sentiment == None:
        sentiment = sentifier.sentiment(demoji_text)
    subjectivity = subjectifier.subjectivity(text)
    num_viewers = int(tweet['user_followers_count'])
    num_reactions = int(tweet['retweet_count']) + int(tweet['favourite_count'])
    return {'sentiment': sentiment, 'subjectivity': subjectivity,
            'num_viewers': num_viewers, 'num_reactions': num_reactions,
            'text': text}


def FindEmoji(text):
    """
    locate emoji in text and
    return demojified text and sentiment
    """
    happy_emoji_count = 0
    sad_emoji_count = 0
    neutral_emoji_count = 0
    emoji_count = 0
    sentiment = None
    # remove emoji
    for emoji in happy_emoji_unicode.values():
        if emoji in text:
            text = text.replace(emoji, '_HAPPY_EMOJI_')
            happy_emoji_count += 1
    for emoji in neutral_emoji_unicode.values():
        if emoji in text:
            text = text.replace(emoji, '_NEUTRAL_EMOJI_')            
            neutral_emoji_count += 1            
    for emoji in sad_emoji_unicode.values():
        if emoji in text:
            text = text.replace(emoji, '_SAD_EMOJI_')            
            sad_emoji_count += 1
    for emoji in emoji_unicode.values():
        if emoji in text:
            text = text.replace(emoji, '_EMOJI_')
    if (sad_emoji_count == 0 and happy_emoji_count > 0): sentiment='pos'
    elif (happy_emoji_count == 0 and sad_emoji_count > 0): sentiment='neg'
    return (text, sentiment)


def WriteGraphData(graph_file, data):
    """append data to graph file"""
    f = open(graph_file, 'a')            
    f.write(data)
    f.close()
    print('\n########################################################')
    print('################# WROTE TO %s  #################' % graph_file)
    print('########################################################\n')    


def WriteSubjectiveTweets(tweet_file, data):
    f = open(tweet_file, 'wb')
    try:
        pickle.dump(data, f, protocol=2)
    except:
        pass
    f.close()

    
def UpdateGraphFile(graph_file, tweet_file, data):
    """output to file, clear buffer"""
    npos = 0
    nneg = 0
    ntweets = 0    
    pos_sentiment = 0
    neg_sentiment = 0
    avg_sentiment = 0
    prevalence = 0
    influence = 0
    most_subjective_tweets = []
    for tweet in data:
        ntweets += 1
        prevalence += tweet['num_viewers']
        influence += tweet['num_reactions']
        if tweet['subjectivity'] > 0:
            if tweet['sentiment'] == 'pos':
                npos += 1
                pos_sentiment += tweet['subjectivity']
            elif tweet['sentiment'] == 'neg':
                nneg += 1
                neg_sentiment -= tweet['subjectivity']
            if tweet['subjectivity'] > 0.95:
                most_subjective_tweets.append([tweet['text'], tweet['sentiment']])
    if npos > 0 or nneg > 0:
        avg_sentiment = int(round((pos_sentiment + neg_sentiment)/(npos + nneg)*100))
    if npos > 0:
        pos_sentiment = int(round(pos_sentiment/npos*100))
    if nneg > 0:
        neg_sentiment = int(round(neg_sentiment/nneg*100))

    polarity = pos_sentiment-neg_sentiment
    prevalence += ntweets
    line = "{}, {}, {}, {}, {}, {}\n".format(pos_sentiment, neg_sentiment, avg_sentiment, polarity, prevalence, influence)
    WriteGraphData(graph_file, line)
    WriteSubjectiveTweets(tweet_file, most_subjective_tweets)
    
    
def ClearGraphData(graph_file):
    """clear data from graph file"""
    f = open(graph_file, 'w')
    f.close()


def main():
    query_id = 0
    TIME_INTERVAL = datetime.timedelta(0, 1) #set time interval to 10 sec
    time_initial = datetime.datetime(1994, 1, 14)
    start_time = time_initial
    end_time = time_initial
    interval_iter = 0
    data_sec = []
    data_min = []
    data_hr = []
    data_day = []
    num_tweets = {'sec': 0, 'min': 0, 'hr': 0, 'day': 0}
    pos_tweets = {'sec': 0, 'min': 0, 'hr': 0, 'day': 0}
    neg_tweets = {'sec': 0, 'min': 0, 'hr': 0, 'day': 0}
    subj_tweets = {'sec': 0, 'min': 0, 'hr': 0, 'day': 0}
    Sentifier = sentification.Sentifier('NB')
    Subjectifier = subjectification.Subjectifier('TextBlob')
    Intensifier = intensification.Intensifier('rule')        
    csvFile = open('{}_tweets.csv'.format(query_id), newline='')
    offset = 0
    fieldnames = ['tweet_id', 'author', 'text', 'date_created',
                  'favourite_count', 'retweet_count', 'user_id',
                  'user_followers_count', 'user_friends_count',
                  'user_tweet_count', 'user_favourites_count',
                  'user_lists_count', 'mention']
    
    """Get system arguments"""
    if (len(sys.argv)) > 1:
        query_id = sys.argv[1]

    """initalise files, clear data"""
    ClearGraphData('{}_sec.txt'.format(query_id))
    ClearGraphData('{}_min.txt'.format(query_id))
    ClearGraphData('{}_hr.txt'.format(query_id))
    ClearGraphData('{}_day.txt'.format(query_id))

    while(1):
        """loop until new data is available"""
        while(1):
            """check offset is equal to sizeof file"""
            while(1):
                """waiting for lock"""
                try:
                    """try to get exclusive lock"""                    
                    fcntl.flock(csvFile, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    break
                except OSError:
                    print('Error: On obtaining lock, sleep, and repeat')
                    time.sleep(0.1) #waiting for lock release

            """
            HAVE LOCK
            check if there is any new data,
            by comparing offset to EOF
            """
            if (offset != csvFile.seek(0, 2)):
                break
            else:
                """"RELEASE LOCK"""
                fcntl.flock(csvFile, fcntl.LOCK_UN)
                time.sleep(0.1)            

        """STILL HAVE LOCK"""
        file_size = csvFile.seek(0, 2)
        csvFile.seek(offset)
        csvReader = csv.DictReader(csvFile, fieldnames=fieldnames)
    
        """load data into temporary buffer"""
        all_tweets= []
        for tweet in csvReader:
            all_tweets.append(tweet)

        """RELEASE LOCK and update offset"""
        fcntl.flock(csvFile, fcntl.LOCK_UN)
        offset = csvFile.tell()

        """process each entry in buffer"""
        for tweet in all_tweets:
            #print(tweet)
            date_created = datetime.datetime.strptime(tweet['date_created'], "%Y-%m-%d %H:%M:%S")
            
            """initialise starting and ending times of interval"""
            if (start_time == time_initial):
                start_time = date_created
                end_time = start_time + TIME_INTERVAL

            """end of interval reached, reset timers"""
            if (date_created > end_time):
                # iterate interval
                interval_iter += 1
                start_time = end_time
                end_time = start_time + TIME_INTERVAL

                """update output files, and reset counters"""
                UpdateGraphFile('{}_sec.txt'.format(query_id), '{}_sec_tweets.pickle'.format(query_id), data_sec) #update every second         
                if (interval_iter % 15 == 0): #update every 15 second
                    pass
                elif (interval_iter % 900 == 0): #update every 15 mins
                    pass
                elif (interval_iter % 3600 == 0): #update every hour
                    pass
                data_sec = []

            """processing data to obtain metrics"""            
            data_sec.append(ProcessTweet(tweet, Sentifier, Subjectifier))
            print('*', end='')
            #print(data_sec[-1])
            
        
    csvFile.close()

if __name__ == "__main__":
    main()
