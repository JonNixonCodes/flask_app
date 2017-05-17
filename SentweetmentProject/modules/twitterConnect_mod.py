#file: twitterConnect_mod.py
import tweepy

consumer_key = 'Mooa8lXLBw64M5zgI3YZOPOCM'
consumer_secret =  'ZwG1ySZFoMecK32FOYolv0Mua0O7WrrxldTmjJWxHmk7NLhl72'
access_token =  '742573307153637377-Po13GoDnUpxS2HC845du1ACW4BmVdqG'
access_token_secret = '520fSVbXVHrjfnSUmItj2xOXOVxANXbXXKArAXvLNGaC2'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# below are useful variables required by scripts which import this module
api = tweepy.API(auth)
