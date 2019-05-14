import json
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

#  Removing stop-words
punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt', 'via']
with open('python.json', 'r') as f:
    #  line = f.readline()  # read only the first tweet/line
    #  tweet = json.loads(line)  # load it as Python dict
    #  print(json.dumps(tweet, indent=4))  # pretty-printi
    count_all = Counter()
    count_search = Counter()
    search_word = "Data"
    com = defaultdict(lambda : defaultdict(int))
    for line in f:
        tweet = json.loads(line)
        #  tokens = preprocess(tweet['text'])
        #  Create a list with all the terms
        terms_all = [term for term in preprocess(tweet['text'])]
        terms_stop = [term for term in preprocess(tweet['text'])
                     if term not in stop]

        # Count terms only once, equivalent to Document Frequency
        terms_single = set(terms_all)
        # Count hashtags only
        terms_hash = [term for term in preprocess(tweet['text'])
                      if term.startswith('#')]
        # Count terms only (no hashtags, no mentions)
        terms_only = [term for term in preprocess(tweet['text'])
                      if term not in stop and
                      not term.startswith(('#', '@'))]
        #  mind the ((double brackets))
        #  startswith() takes a tuple (not a list) if
        #  we pass a list of inputs

        if search_word in terms_only:
            count_search.update(terms_only)

        #  Term co-occurrences
        #  Build co-occurrence matrix
        for i in range(len(terms_only)-1):
            for j in range(i+1, len(terms_only)):
                w1, w2 = sorted([terms_only[i], terms_only[j]])
                if w1 != w2:
                    com[w1][w2] += 1

        terms_bigram = bigrams(terms_stop)

        #  Update the counter
        count_all.update(terms_bigram)
        #  print(tokens)

    com_max = []
    # For each term, look for the most common co-occurrent terms
    for t1 in com:
        t1_max_terms = sorted(com[t1].items(), key=operator.itemgetter(1), reverse=True)[:5]
        for t2, t2_count in t1_max_terms:
            com_max.append(((t1, t2), t2_count))
    # Get the most frequent co-occurrences
    terms_max = sorted(com_max, key=operator.itemgetter(1), reverse=True)
    print(terms_max[:5])

    print("Co-occurrence for %s:" % search_word)
    print(count_search.most_common(20))
    word_freq = count_search.most_common(20)
    labels, freq = zip(*word_freq)
    data = {'data': freq, 'x': labels}
    bar = vincent.Bar(data, iter_idx='x')
    bar.to_json('term_freq.json')


    #  Print the first 5 most frequent words
    print(count_all.most_common(5))


