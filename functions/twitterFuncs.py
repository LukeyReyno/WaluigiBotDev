import typing
import tweepy
import json

# Initialize Credentials for Twitter
class TwitterCredentials():
    def __init__(self, twitterCredDict):
        self.__dict__ = twitterCredDict

with open("data/twitterAuth.json", "r") as twitterCredJSON:
    credDict = json.load(twitterCredJSON)

TC = TwitterCredentials(credDict)

auth = tweepy.OAuthHandler(TC.consumer_key, TC.consumer_secret)
auth.set_access_token(TC.access_token, TC.access_token_secret)

# create api Client instance
twitterClient = tweepy.API(auth)

def fetchMostRecentTweetURL(user_search: str):
    user_search = user_search.strip("@")
    userList = twitterClient.search_users(user_search)
    if len(userList) < 1:
        return "`No Users Found`"
    foundUser: tweepy.User = userList[0]
    tweetList = foundUser.timeline()
    if len(tweetList) < 1:
        return f"`Found User, @{foundUser.screen_name}, has no tweets on their timeline.`"
    tweet: tweepy.Status = tweetList[0]
    return f"https://twitter.com/{foundUser.screen_name}/status/{tweet.id}"
