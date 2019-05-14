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

import math

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
    # URLs
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',

    r'(?:(?:\d+,?)+(?:\.?\d+)?)',  # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])",  # words with - and '
    r'(?:[\w_]+)',  # other words
    r'(?:\S)'  # anything else
]

tokens_re = re.compile(r'(' + '|'.join(regex_str) + ')',
                       re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^' + emoticons_str + '$',
                         re.VERBOSE | re.IGNORECASE)


def tokenize(s):
    return tokens_re.findall(s)


def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else
                  token.lower() for token in tokens]
    return tokens


#  Sentimental analysis
p_t = {}
p_t_com = defaultdict(lambda: defaultdict(int))
com = defaultdict(lambda: defaultdict(int))
pmi = defaultdict(lambda: defaultdict(int))
#  Removing stop-words
punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt', 'via']

# get number line in a file


def file_lengthy(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
        return i + 1


if __name__ == '__main__':
    fname = 'python.json'

    #  n_docs is the total number of tweets that you have collected
    #  JSON Lines file as described in the previous articles,
    #  it’s essentially the total number of lines in that file
    n_docs = file_lengthy(fname)
    print(n_docs)

    #  Reading tweets
    with open(fname, 'r') as f:
        count_search = Counter()
        search_word = "Python"
        com = defaultdict(lambda: defaultdict(int))
        for line in f:
            tweet = json.loads(line)
            # Count terms only (no hashtags, no mentions)
            terms_only = [term for term in preprocess(tweet['text'])
                          if term not in stop
                          and not term.startswith(('#', '@', 'http'))
                          and len(term) > 2]

            # print(terms_only)
            if search_word in terms_only:
                count_search.update(terms_only)

            #  Term co-occurrences
            #  Build co-occurrence matrix
            for i in range(len(terms_only) - 1):
                for j in range(i + 1, len(terms_only)):
                    w1, w2 = sorted([terms_only[i], terms_only[j]])
                    if w1 != w2:
                        com[w1][w2] += 1

        #  Computing Term Probabilities
        #  print(count_search)
        for term, n in count_search.items():
            p_t[term] = n / n_docs
            #  print(com[term])
            for t2 in com[term]:
                p_t_com[term][t2] = com[term][t2] / n_docs

        #  print(p_t_com)
        #  two vocabularies for positive and negative terms
        positive_vocab = ['good', 'nice', 'great', 'awesome', 'outstanding',
                          'fantastic', 'terrific', ':)', ':-)', 'like', 'love']

        negative_vocab = ['bad', 'terrible', 'crap', 'useless', 'hate', ':(',
                          ':-(']

        #  compute the PMI of each pair of terms, and then compute the
        #  Semantic Orientation
        #  print(p_t)
        for t1 in p_t:
            for t2 in com[t1]:
                denom = p_t[t1] * p_t[t2]
                pmi[t1][t2] = math.log2(p_t_com[t1][t2] / denom)

        semantic_orientation = {}
        for term, n in p_t.items():
            positive_assoc = sum(pmi[term][tx] for tx in positive_vocab)
            negative_assoc = sum(pmi[term][tx] for tx in negative_vocab)
            semantic_orientation[term] = positive_assoc - negative_assoc

        #  semantic orientation for some terms
        semantic_sorted = sorted(semantic_orientation.items(),
                                 key=operator.itemgetter(1),
                                 reverse=True)
        top_pos = semantic_sorted[:10]
        top_neg = semantic_sorted[-10:]

        print(top_pos)
        print(top_neg)
        #  print(semantic_orientation)
        print("#Python: %f" % semantic_orientation['Python'])
