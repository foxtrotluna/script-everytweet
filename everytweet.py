# Every tweet - by Luna Winters
# This bot will tweet every tweet available to the public. In order.
#
#The MIT License (MIT)
#
#Copyright (c) 2015 Luna Winters
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.
from __future__ import absolute_import, print_function

import sys
import tweepy
import time
import html.parser

# == OAuth Authentication ==
#
# This mode of authentication is the new preferred way
# of authenticating with Twitter.

# The consumer keys can be found on your application's Details
# page located at https://dev.twitter.com/apps (under "OAuth settings")
consumer_key=""
consumer_secret=""

# The access tokens can be found on your applications's Details
# page located at https://dev.twitter.com/apps (located
# under "Your access token")
access_token=""
access_token_secret=""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.secure = True
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

lastfile = open("lasttried.txt","r+")
tweetid = int(lastfile.read())
html_parser = html.parser.HTMLParser() #Will decode HTML chars as twitter encodes them

while True:
    tweetid += 1
    lastfile.seek(0)
    lastfile.write(str(tweetid))
    try:
        tweet = api.get_status(tweetid)
        #Unescape the HTML chars then replace @ symbols with + signs to combat spamminess
        text = html_parser.unescape(tweet.text).replace("@","+")
        print(str(tweetid) + ": " + text)
        api.update_status(text)
        time.sleep(120)
    except tweepy.error.TweepError:
        print(str(tweetid) + ": Invalid ID")
        time.sleep(1) #So it'll not exceed the rate limit
