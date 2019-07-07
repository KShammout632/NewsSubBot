import tweepy, tkinter
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import json

consumer_key = 'xxxx'
consumer_secret = 'xxxx'
access_token = 'xxxx'
access_token_secret = 'xxxx'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

user = api.me()
print(user.name)

def retweet5():
    search = "nature"
    numOfTweets = 5
    for tweet in tweepy.Cursor(api.search, search).items(numOfTweets):
        try:
            tweet.retweet()
            print("Retweeted the tweet: " + tweet.text)
        except tweepy.TweepError as e:
            print(e.reason)
        except StopIteration:
            break

def printFavs():
    for s in api.favorites():
        try:
            print("Desc: " + s.text_extended)
            print("With " + str(s.favorite_count) + " favourites")
        except tweepy.TweepError as e:
            print(e.reason)
        except StopIteration:
            break


#url = 'http://web.mta.info/developers/turnstile.html'
url = 'https://www.bbc.com/news/world'
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

with open('newsSub.json', 'r') as json_file:
    data = json.load(json_file)

def getHeader():
    desc = ""
    link = ""
    s1 = soup.find("a", class_="gs-c-promo-heading gs-o-faux-block-link__overlay-link gel-pica-bold nw-o-link-split__anchor")
    allHeaders = soup.find_all("a", class_="gs-c-promo-heading gs-o-faux-block-link__overlay-link gel-pica-bold nw-o-link-split__anchor")
    for header in allHeaders:
        desc = header.string
        #desc = "rebuild"
        if(desc != None):
            (key,val) = getMatchingWord(desc)
        if(desc != None and val != ""):
            print("Title of article: " + desc)
            #print(getMatchingWord(desc))
            tweetOut(header,key)
            break

def tweetOut(header,key):
    desc = header.string
    prevLink = header.find_parents("a")
    print(prevLink)
    #link = prevLink.href
    ind = desc.index(key)
    val = data.get(key)
    valLen = len(val)
    outT = desc[:ind] + val + desc[ind+valLen:]
    print(outT)
    API.update_status("From BBC: " + outT)
    #print("Original article: " + str(link))

def getMatchingWord(s):
    for p in data:
        if(p in s):
            return (p,data.get(p))
    #json_file = None
    return ("","")

def main():
    (x,y) = getMatchingWord("rebuild")
    print(x,y)
    getHeader()

main()
