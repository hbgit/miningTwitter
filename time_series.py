import json
import pandas
import re
import operator
import nltk
from nltk import bigrams
from nltk.tokenize import word_tokenize
from collections import Counter
from nltk.corpus import stopwords
import string

from collections import defaultdict

import vincent

#  nltk.download()

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


#  Removing stop-words
punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt', 'via']
with open('python.json', 'r') as f:
    dates_python = []
    dates_data = []
    dates_aws = []
    for line in f:
        tweet = json.loads(line)
        # let's focus on hashtags only at the moment
        terms_hash = [term for term in preprocess(tweet['text']) if term.startswith('#')]
        # track when the hashtag is mentioned
        if '#python' in terms_hash:
            dates_python.append(tweet['created_at'])
        if '#data' in terms_hash:
            dates_data.append(tweet['created_at'])
        if '#AWS' in terms_hash:
            dates_aws.append(tweet['created_at'])



    #  a list of "1" to count the hashtags
    ones_python = [1]*len(dates_python)
    ones_data = [1]*len(dates_data)
    ones_aws = [1]*len(dates_aws)
    #  the index of the series
    idx_python = pandas.DatetimeIndex(dates_python)
    idx_data = pandas.DatetimeIndex(dates_data)
    idx_aws = pandas.DatetimeIndex(dates_aws)
    #  the actual series (at series of 1s for the moment)
    python = pandas.Series(ones_python, index=idx_python)
    data = pandas.Series(ones_data, index=idx_data)
    aws = pandas.Series(ones_aws, index=idx_aws)
    #  Resampling / bucketing
    per_minute_p = python.resample('1Min').sum().fillna(0)
    per_minute_d = data.resample('1Min').sum().fillna(0)
    per_minute_a = aws.resample('1Min').sum().fillna(0)

    #  time_chart = vincent.Line(python)
    #  time_chart.axis_titles(x='Time', y='Freq')
    #  time_chart.to_json('time_chart.json')

    # all the data together
    match_data = dict(python=per_minute_p, data=per_minute_d, aws=per_minute_a)
    # we need a DataFrame, to accommodate multiple series
    all_matches = pandas.DataFrame(data=match_data, index=per_minute_p.index)
    # Resampling as above
    all_matches = all_matches.resample('1Min').sum().fillna(0)
    print(all_matches)

    # and now the plotting
    time_chart = vincent.Line(all_matches[['python', 'data', 'aws']])
    time_chart.axis_titles(x='Time', y='Freq')
    time_chart.legend(title='Matches')
    time_chart.to_json('time_chart.json')



