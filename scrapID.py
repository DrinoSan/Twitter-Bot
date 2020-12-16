import tweepy
import logging
from config import create_api
import json
from twitterUsers import users

# Scrapping of all the users in twitterUsers.py the IDs
# Returns the list of all user IDs


def scrap(api):

    list_of_IDs = []
    # for user in users:
    # list_of_IDs.append(str(api.get_user(user).id))
    list_of_IDs = [str(api.get_user(userid).id) for userid in users]

    return list_of_IDs
