from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize

sentences = ["VADER is smart, handsome, and funny.", # positive sentence example
"VADER is smart, handsome, and funny!", # punctuation emphasis handled correctly (sentiment intensity adjusted)
"VADER is very smart, handsome, and funny.",  # booster words handled correctly (sentiment intensity adjusted)
"VADER is VERY SMART, handsome, and FUNNY.",  # emphasis for ALLCAPS handled
"Most automated sentiment analysis tools are shit.",
"VADER sentiment analysis is the shit.",
"Sentiment analysis has never been good.",
"Sentiment analysis with VADER has never been this good.",
"Warren Beatty has never been so entertaining."]

sid = SentimentIntensityAnalyzer()
for sentence in sentences:
    print(sentence)
    ss = sid.polarity_scores(sentence)
    for k in sorted(ss):
        print('{0}: {1}, '.format(k, ss[k]), end='')
    print()
