import praw
import time
import datetime
import sys

# This bot will log into Reddit and post any links that you want at a specific time.
# It lets you schedule the first post to be within 24 hours of the current time, 
# and then you can set the interval between every post from there on out.
# You can also x-post with this bot and all x-posts will be submitted at the same time.
# The titles will be the same for each one though, so if you want them to be different, 
# just make them separate posts. That means the x-posts will be posted later than the original, 
# but that's never been an issue for me so I never bothered fixing that.
# This bot also does not check for captcha, and it assumes that you already have enough subreddit karma
# to post there.

# 'posts' file format:
# Post title
# Post URL
# Subreddit(s) (Separated by spaces)
# Repeat for all posts

#Make your own profile file 'intervalPostBotProfile' with all these variables for oauth 2
from intervalPostBotProfile import APP_UA
from intervalPostBotProfile import app_id
from intervalPostBotProfile import app_secret
from intervalPostBotProfile import app_uri
from intervalPostBotProfile import app_scopes
from intervalPostBotProfile import app_account_code
from intervalPostBotProfile import APP_REFRESH

r =                 praw.Reddit(APP_UA)
title =             ''      # temporary variable for appending titles into array
URL =               ''      # temporary variable for appending URLs into array
subreddit =         []      # temporary variable for appending subreddits into array
TIMEHOUR =          4       # hour time to post (24 hour time)
TIMEMINUTE =        20      # minute time to post
POSTDELAY =         10      # seconds between each post

def login():
    # Logs into Reddit and will tell you if everything works.
    print("Logging into reddit")
    r.set_oauth_app_info(app_id, app_secret, app_uri)
    r.refresh_access_information(APP_REFRESH)
    print("Log in successful")
    return r

def testposter():
    # Reads the posts file and prints out all the posts.
    # Use this to check if your file has any mistakes.
    postsfile =     open('posts')           # file containing all the posts
    typeOfLine =    1;                      # Used to sort the lines properly
    # sorts input into correct array
    for line in postsfile:
        line = line.rstrip('\n')            # removes \n from line
        if typeOfLine == 1:                 # post title
            title = line
        elif typeOfLine == 2:               # URL
            URL = line
        elif typeOfLine == 3:               # subreddit; loads in multiple subreddits with titles/URLs if necessary; also submits the post
            subreddit = line.split()
            typeOfLine = 0                  # resets typeOfLine because we move on to a new post
            for sr in subreddit:
                print(URL + " (" + title + ") going to /r/" + sr)
            subreddit[:] = []
        typeOfLine += 1                     # move on to next line type

def postbot():
    
    for i in xrange(0,365):
        # sleeps until TIMEHOUR:TIMEMINUTE
        t = datetime.datetime.today()
        future = datetime.datetime(t.year,t.month,t.day,TIMEHOUR,TIMEMINUTE)
        if t.hour >= TIMEHOUR and t.minute >= TIMEMINUTE:
            future += datetime.timedelta(days=1)
        print("wait until " + str(TIMEHOUR) + ":" + str(TIMEMINUTE) + "AM")
        time.sleep((future-t).seconds)
        # posts everything
        postsfile =     open('posts')           # file containing all posts
        typeOfLine =    1;                      # see above; sorts lines
        # sorts input into correct array
        for line in postsfile:
            line = line.rstrip('\n')            # removes \n from line
            if typeOfLine == 1:                 # post title
                title = line
            elif typeOfLine == 2:               # URL
                URL = line
            elif typeOfLine == 3:               # subreddit; loads in multiple subreddits with titles/URLs if necessary; also submits the post
                subreddit = line.split()
                typeOfLine = 0                  # resets typeOfLine because we move on to a new post
                for sr in subreddit:
                    print("posting post " + URL + " (" + title + ") to /r/" + sr)
                    r.submit(sr, title, url=URL)# post line
                    time.sleep(POSTDELAY)
                subreddit[:] = []               # resets subreddit list for next post
            typeOfLine += 1                     # move on to next line type

# Uncomment whichever is necessary:
# Only uncomment testposter() to test if your 'posts' file is correct
# Only uncomment login() and postbot() to post
#login()
#testposter()
#postbot()