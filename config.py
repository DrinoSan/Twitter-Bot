
import tweepy
import logging
import os

logger = logging.getLogger()

# Function to connect to Twitter
# Check this out for more informations regarding the authentification : https://developer.twitter.com/en/docs/basics/getting-started
# Tweepy Auth docs http://docs.tweepy.org/en/v3.5.0/auth_tutorial.html#auth-tutorial
# returns the API Object


def create_api():

    # Insert your Keys in this area
    # https://developer.twitter.com/en/docs/labs/covid19-stream/quick-start
    consumer_key = 'YOU CONSUMER KEY'
    consumer_secret = 'Secret'
    access_token = 'token'
    acess_token_secret = 'other token'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, acess_token_secret)

    # API OBJECT
    # Docs for more informations
    # http://docs.tweepy.org/en/v3.5.0/api.html
    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)

    try:
        api.verify_credentials()
        print("Authentication OK")
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api
