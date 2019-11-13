import tweepy, tkinter
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import json
import config


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

def getHeaderBBC():
    desc = ""
    link = ""
    with open('visited.txt','r') as f:
        visited = f.read()
    allHeaders = soup.find_all("a", class_="gs-c-promo-heading gs-o-faux-block-link__overlay-link gel-pica-bold nw-o-link-split__anchor")
    for header in allHeaders:
        desc = header.string
        if(desc != None):
            desc = desc.lower()
            (key,val) = getMatchingWord(desc)
            if(val != ""):
                newDesc = desc.replace(key, val)
                print(newDesc)
                link = "https://www.bbc.com" + header['href']
                print(link)
                if(link not in visited):
                    print("tweet")
                    tweetOut(newDesc,link)
                    break



def tweetOut(desc,link):
    with open('temp.txt', 'w') as f:
        f.write("From BBC: " + desc + "\n " + link)

    with open('temp.txt','r') as f:
        api.update_status(f.read())

    open('temp.txt', 'w').close()

    with open('visited.txt', 'a') as f:
        f.write(link + "\n")


def getMatchingWord(s):
    for p in data:
        if(p in s):
            return (p,data.get(p))
    return ("","")

def main():
    getHeaderBBC()

url = 'https://www.bbc.com/news/world'
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

with open('newsSub.json', 'r') as json_file:
    data = json.load(json_file)

auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)
api = tweepy.API(auth)

user = api.me()
print(user.name)
print("logged in!")

main()
