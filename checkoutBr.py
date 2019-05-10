# based on
# https://marcobonzanini.com/2015/03/02/mining-twitter-data-with-python-part-1/
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

import json

consumer_key = 'JrbRH8jC5HpyM9UUUdlQ5ughC'
consumer_secret = 'tBCdiHt04nvoWP5NMm62uJFFYl1L2SUbhvh2Ri7XaGYkyzNewm'
access_token = '24904823-0rviVLPKT0FzZPXEcvN7igxan5pwS8TlQhXmQH5ON'
access_secret = 'd0jQIhXTneYIczCwcUIApdF3rUMOnpEPYck8LfGjTa8IS'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

# for status in tweepy.Cursor(api.home_timeline).items(10):
#    print(status.text)


def process_or_store(tweet):
    print(json.dumps(tweet))


# gather all the upcoming tweets about a particular event, the streaming API
# gathers all the new tweets with the #python hashtag
class MyListener(StreamListener):

    def on_data(self, data):
        try:
            with open('python.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True


twitter_stream = Stream(auth, MyListener())
twitter_streamtwitter_stream.filter(track=['#python'])
