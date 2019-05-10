import json
from nltk.tokenize import word_tokenize
import re

emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""

regex_str = [
    emoticons_str,
    r'<[^>]+>',  # HTML tags
    r'(?:@[\w_]+)',  # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",  # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',  # URLs

    r'(?:(?:\d+,?)+(?:\.?\d+)?)',  # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])",  # words with - and '
    r'(?:[\w_]+)',  # other words
    r'(?:\S)'  # anything else
]

tokens_re = re.compile(r'('+'|'.join(regex_str)+')',
                       re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)


def tokenize(s):
    return tokens_re.findall(s)


def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else
                  token.lower() for token in tokens]
    return tokens


"""
The key attributes are the following:

text: the text of the tweet itself
created_at: the date of creation
favorite_count, retweet_count: the number of favourites and retweets
favorited, retweeted: boolean stating whether the authenticated user (you)
                      have favourited or retweeted this tweet
lang: acronym for the language (e.g. “en” for english)
id: the tweet identifier
place, coordinates, geo: geo-location information if available
user: the author’s full profile
entities: list of entities like URLs, @-mentions, hashtags and symbols
in_reply_to_user_id: user identifier if the tweet is a reply to a specific user
in_reply_to_status_id: status identifier id the tweet is a reply to a specific
                        status

"""

with open('python.json', 'r') as f:
    #  line = f.readline()  # read only the first tweet/line
    #  tweet = json.loads(line)  # load it as Python dict
    #  print(json.dumps(tweet, indent=4))  # pretty-printi
    for line in f:
        tweet = json.loads(line)
        tokens = preprocess(tweet['text'])
    #  do_something_else(tokens)
        print(tokens)
