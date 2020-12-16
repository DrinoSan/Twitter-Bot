import tweepy
import logging
from config import create_api
import json
from twitterUsers import users, search_terms
from scrapID import scrap

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# Docs: http://docs.tweepy.org/en/v3.9.0/streaming_how_to.html
# Code: https://github.com/tweepy/tweepy/tree/master/tweepy
# Twitter Status codes: https://developer.twitter.com/en/docs/basics/response-codes

class FavRetweetListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api


    def on_status(self, tweet):
        logger.info("Processing tweet id {}".format(tweet.id))
        #logger.info(f"Name of Processing tweet: {tweet.user.screen_name}")
        #logger.info(f"Hashtags of tweet: {type(tweet.entities['hashtags'])}")


        # Checking Hashtags in tweet and adds hashtags to newList
        newList = []
        if len(tweet.entities['hashtags']) > 0:
            for i in tweet.entities['hashtags']:
                newList.append(i['text'])
                
        logger.info("HASHTAGS in the Tweet: {}".format(newList))
        logger.info('USER ID: {} and USER NAME: {}'.format(tweet.user.id, tweet.user.screen_name))
                

        for userss in users:
            try:
                # Checking if hashtags match with search_terms
                result =  any(elem in newList  for elem in search_terms)
                if result: 
                    if tweet.user.screen_name == userss:
                        print("user.screen_name = {}".format(tweet.user.screen_name))
                        print("userss = {}".format(userss))
                        if not tweet.favorited:
                            try:
                                # Favorite tweet if not already
                                tweet.favorite()
                            except tweepy.TweepError as e:
                                logger.info("TWEEPY Error code with Fav: {}".format(e))
                        if not tweet.retweeted:
                            try:
                                # Retweet if not already retweeted
                                tweet.retweet()
                            except tweepy.TweepError as e:
                                logger.info("TWEEPY Error code with Retweet: {}".format(e))
                else:
                    pass
            except tweepy.TweepError as e:
                logger.info("Other Errors: {}".format(e))
        
        newList.clear()


    def on_error(self, status):
        logger.error(status)

def main():
    api = create_api()
    user_IDs = scrap(api)
    tweets_listener = FavRetweetListener(api)
    stream = tweepy.Stream(api.auth, tweets_listener)
    try:
        stream.filter(track=search_terms, follow=user_IDs, languages=['en', 'de'])
    except Exception as e:
        logger.info("Fehler beim Stream FEHLER:  {}".format(e))



if __name__ == "__main__":
    main()
