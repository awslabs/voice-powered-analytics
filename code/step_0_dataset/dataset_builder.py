import boto3
from boto3 import resource
import json
import tweepy
import logging
import os
from tweepy import OAuthHandler

consumer_key = os.environ.get('CONSUMER_KEY')
consumer_secret = os.environ.get('CONSUMER_SECRET')
access_token = os.environ.get('ACCESS_TOKEN')
access_secret = os.environ.get('ACCESS_SECRET')

ddbtable = os.environ.get("VPA_TWITTER_STATE_TABLE")
fhstream = os.environ.get("TWEETS_FH_STREAM")
search_text = os.environ.get("SEARCH_TEXT")
max_tweets = int(os.environ.get("MAX_TWEETS"))
Records = []

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)
session = boto3.Session()
firehoseclient = session.client('firehose')
dynamodb_resource = resource('dynamodb')
table = dynamodb_resource.Table(ddbtable)
logger = logging.getLogger()


def send_to_fh():
    firehoseclient.put_record_batch(DeliveryStreamName=fhstream, Records=Records)
    logger.info("Sent {0} records to firehose".format(len(Records)))
    Records.clear()


def lambda_handler(event, context):
    response = table.get_item(Key={'name': 'latest'})
    try: 
        sinceid = int(response['Item']['sinceid'])
        logger.info("Sinceid from last run was {0}".format(sinceid))
    except KeyError as error:
        #if running on first iteration
        logger.info("Setting sinceId to 0 on first iteration")
        sinceid = 0
    tweet_count = 0
    spamCount = 0

    for tweet in tweepy.Cursor(api.search, q=search_text, result_type="recent", include_entities=False, count=100, since_id=sinceid).items(max_tweets):
        t = {}
        t['id'] = tweet.id
        t['text'] = tweet.text
        t['created'] = tweet.created_at.strftime('%Y-%m-%d %H:%M:%S')
        user = tweet.user
        t['screen_name'] = user.screen_name
        t['screen_name_followers_count'] = user.followers_count
        if tweet.place is not None:
            place = tweet.place
            t['country'] = place.country
            t['place'] = place.full_name
        else:
            t['place'] = "none"
            t['country'] = "none"
        t['retweet_count'] = tweet.retweet_count
        t['favorite_count'] = tweet.favorite_count

        r = {'Data': json.dumps(t) + "\n"}

        tweet_count += 1
        # prevent spam using the same #reinvent hashtag
        findnum = t['screen_name'].find('Affgenius')
        if findnum > 0:
            print(findnum)
        if ((t['screen_name'].find('Affgenius') >= 0)
            or (t['screen_name'].find('AffgeniusMarket') >= 0)
            or (t['text'].find('Affgenius') >= 0)
            or (t['text'].find('#REGA') >= 0)
            ):
            spamCount += 1
        else:
            Records.insert(len(Records), r)

        if sinceid < tweet.id:
            sinceid = tweet.id

        if (tweet_count % 500) == 0:
            send_to_fh()

    if len(Records) > 0:
        send_to_fh()

    logger.info("Saving sinceid of {0}".format(sinceid))
    table.put_item(Item={'name': 'latest', 'sinceid': sinceid})
    logger.info("Downloaded {0} tweets".format(tweet_count))
    logger.info("Sinceid for next run: {0}".format(sinceid))

    return {'message': "Downloaded {0} tweets, {1} were spam".format(tweet_count, spamCount)}


# if you want to call outside of lambda
# lambda_handler("event", "context")
