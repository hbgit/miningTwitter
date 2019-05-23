import json
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import datetime

consumer_key = 'JrbRH8jC5HpyM9UUUdlQ5ughC'
consumer_secret = 'tBCdiHt04nvoWP5NMm62uJFFYl1L2SUbhvh2Ri7XaGYkyzNewm'
access_token = '24904823-0rviVLPKT0FzZPXEcvN7igxan5pwS8TlQhXmQH5ON'
access_secret = 'd0jQIhXTneYIczCwcUIApdF3rUMOnpEPYck8LfGjTa8IS'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)

# Checkout https://www.programcreek.com/python/example/76301/tweepy.Cursor
# startDate = datetime.datetime(2019, 5, 14, 0, 0, 0)
# endDate = datetime.datetime(2019, 5, 16, 0, 0, 0)

date = ('2019-05-14', '2019-05-16')


def search_tweets(keyword):
    # api = authentication(CONS_KEY, CONS_SECRET, ACC_TOKEN, ACC_SECRET)
    for tweet in tweepy.Cursor(api.search,
                               q=keyword,
                               since=date[0],
                               until=date[1],
                               show_user=True).items():
        try:
            with open('greve_141516.json', 'a', encoding='utf8') as file:
                #json.dump(tweet._json, file)
                json.dump(tweet._json, file, indent=4)
        except tweepy.TweepError as e:
            print(e.reason)
            sleep(900)
            continue
        except StopIteration:  # stop iteration when last tweet is reached
            break


keyword = "greve"
tweets = search_tweets(keyword)

# for tweet in tweets.items():
#    print("ID TWEET: " + str(tweet.id))

# print(len(list(tweets.items())))

# print(json.dumps(tweets))
