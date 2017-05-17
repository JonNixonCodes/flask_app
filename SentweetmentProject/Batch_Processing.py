#!/usr/bin/env python3.4
import csv
import datetime
import time
#dealing with deadlock
import fcntl
import sys
import os
directories = os.getcwd().split('/')
if directories[-1] == 'flask_app':
    sys.path.append('SentweetmentProject/modules')
else:
    sys.path.append('modules')

import sentification_mod as sentification
import subjectification_mod as subjectification
import intensification_mod as intensification

def ProcessTweet(text, sentifier, subjectifier, intensifier):
    sentiment = sentifier.sentiment(text)
    confidence = sentifier.confidence(text)
    subjectivity = subjectifier.subjectivity(text)
    intensity = intensifier.intensity(text)
    return (sentiment, confidence, subjectivity, intensity)

import nltk
from nltk.tokenize import word_tokenize, RegexpTokenizer, TweetTokenizer, WhitespaceTokenizer

import pickle
import emoji
from emoji import UNICODE_EMOJI, EMOJI_UNICODE

"""
Hacky solution to running script from different directory
"""
import os
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

def FindEmoji(text):
    happy_emoji_count = 0
    sad_emoji_count = 0
    neutral_emoji_count = 0
    emoji_count = 0
    
    text = emoji.demojize(text)
    # remove emoji
    regTokenizer = RegexpTokenizer('\s+', gaps=True)
    tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True, reduce_len=True)
    words = regTokenizer.tokenize(text)
    for w in words:
        if w in emoji_unicode.keys():
            if w in neutral_emoji_unicode.keys():
                neutral_emoji_count += 1
                text = text.replace(w, '__NEUTRAL_EMOJI__', 1)
            elif w in happy_emoji_unicode.keys():
                happy_emoji_count += 1
                text = text.replace(w, '__HAPPY_EMOJI__', 1)
            elif w in sad_emoji_unicode.keys():
                sad_emoji_count += 1
                text = text.replace(w, '__SAD_EMOJI__', 1)
            else:
                emoji_count += 1
                text = text.replace(w, '__EMOJI__')
        retVal = 0
        if happy_emoji_count > 0 and sad_emoji_count == 0:
            retVal = 1
        elif sad_emoji_count > 0 and happy_emoji_count == 0:
            retVal = -1
    return (text, retVal)

def WriteGraphData(graph_file, data):
    f = open(graph_file, 'a')            
    f.write(data)
    f.close()
    print('\n\n########################################################')
    print('################ WROTE TO %s  ################' % graph_file)
    print('########################################################\n\n')    

def ClearGraphData(graph_file):
    f = open(graph_file, 'w')
    f.close()
    
# main
"""
Get system arguments
"""
if (len(sys.argv)) > 0:
    query_id = sys.argv[1]
else:
    query_id = 0
    
TIME_INTERVAL = datetime.timedelta(0, 1) #set time interval to 10 sec
#start_time = datetime.datetime.now()
time_initial = datetime.datetime(1994, 1, 14)
start_time = time_initial
end_time = time_initial
interval_iter = 0
num_tweets = 0
pos_tweets = 0
neg_tweets = 0
subj_tweets = 0

#initialise files, and clear data
ClearGraphData('{}_sec.txt'.format(query_id))
ClearGraphData('{}_min.txt'.format(query_id))
ClearGraphData('{}_hr.txt'.format(query_id))
ClearGraphData('{}_day.txt'.format(query_id))

Sent = sentification.Sentifier('NB')
Subj = subjectification.Subjectifier('TextBlob')
Intens = intensification.Intensifier('rule')
csvFile = open('{}_tweets.csv'.format(query_id), newline='')
offset = 0

while(1):
    #loop until new data is available
    #while offset is equal to sizeof file
    while(1):
        #try to get lock
        while(1):
            try:
                #try to obtain exclusive lock
                fcntl.flock(csvFile, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except OSError:
                print('Error: On obtaining lock, sleep, and repeat')
                #waiting for lock release
                time.sleep(0.1)

        #HAVE LOCK
        #check if any new data
        #by comparing offset to EOF
        if (offset != csvFile.seek(0, 2)):
            break
        else:
            #RELEASE LOCK
            fcntl.flock(csvFile, fcntl.LOCK_UN)
            time.sleep(0.1)
            

    #STILL HAVE LOCK
    file_size = csvFile.seek(0, 2)
    csvFile.seek(offset)
    csvReader = csv.DictReader(csvFile, fieldnames = ['author', 'text', 'date_created', 'favourited', 'retweeted'])
    
    # load tweets into temporary buffer
    buffer = []
    for row in csvReader:
        #print(row)
        author = row['author']
        date_created = datetime.datetime.strptime(row['date_created'], "%Y-%m-%d %H:%M:%S")
        text = row['text']
        buffer.append({'author': author, 'date_created': date_created, 'text': text})

    #RELEASE LOCK
    fcntl.flock(csvFile, fcntl.LOCK_UN)
    
    #set offset in csv file
    offset = csvFile.tell()

    # process each entry in buffer
    for entry in buffer:
        author = entry['author']
        date_created = entry['date_created']
        text = entry['text']
        # initialise start_time, end_time
        if (start_time == time_initial):
            start_time = date_created
            end_time = start_time + TIME_INTERVAL
        if (date_created > end_time):
            # iterate interval
            interval_iter += 1
            # reset time interval
            start_time = end_time
            end_time = start_time + TIME_INTERVAL
            # update graph_data.txt
            sentval = int(pos_tweets/(pos_tweets + neg_tweets)*100)
            subjval = int(subj_tweets/(num_tweets)*100)
            line = "{0}, {1}, {2}\n".format(interval_iter, sentval, subjval)
            
            #write to graph data to file
            if (interval_iter % 15 == 0):
                WriteGraphData('{}_min.txt'.format(query_id), line)
            elif (interval_iter % 900 == 0):
                WriteGraphData('{}_hr.txt'.format(query_id), line)
            elif (interval_iter % 3600 == 0):
                WriteGraphData('{}_day.txt'.format(query_id), line)
            WriteGraphData('{}_sec.txt'.format(query_id), line)
            
            # reset counters
            num_tweets = 0
            pos_tweets = 0
            neg_tweets = 0
            subj_tweets = 0
            assert date_created <= end_time                        

        # find emojis
        text, emoji_val = FindEmoji(text)
        # calculating sentiment and confidence and subjectivity
        subjectivity = 1.0
        confidence = 1.0
        if emoji_val == 1:
            sentiment = 'pos'
        elif emoji_val == -1:
            sentiment = 'neg'
        else:
            sentiment, confidence, subjectivity, intensity = ProcessTweet(text, Sent, Subj, Intens)
            """
            if intensity > 0:
                # printing shit
                print('Author: ', author)
                print('Date Created: ', date_created)
                print('Text: ', text)
                print('Subjectivity: ', str(subjectivity))
                print('Sentiment: ', sentiment)
                print('Confidence: ', str(confidence))
                print('Intensity: ', str(intensity), '\n')
            """
        if sentiment == 'pos':
            pos_tweets += 1
            subj_tweets += 1
        else:
            neg_tweets += 1
            subj_tweets += 1
    
        # updating counters
        num_tweets += 1
        
csvFile.close()
