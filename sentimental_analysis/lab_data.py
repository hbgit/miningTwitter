# Clean data https://medium.com/free-code-camp/how-to-make-your-own-sentiment-analyzer-using-python-and-googles-natural-language-api-9e91e1c493e
# Labeling our Data
"""
NLTK’s built-in Vader Sentiment Analyzer will simply rank a piece of text
as positive, negative or neutral using a lexicon of positive and negative words.
"""

from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import json
import pandas as pd
from pprint import pprint
import matplotlib.pyplot as plt
import seaborn as sns

import numpy as np
from matplotlib import colors
from matplotlib.ticker import PercentFormatter

tweets_data_path = '../stream_tuto/twitter_data.json'

tweets_data = []
# reading the JSON data using json.load()
with open(tweets_data_path, 'r') as f:
    for line in f:
        tweet = json.loads(line)
        tweets_data.append(tweet)

# converting json dataset from dictionary to dataframe
tweets = pd.DataFrame(tweets_data)

#print(tweets['text'].head())

sia = SIA()
results = []

for tw in tweets['text']:
    pol_score = sia.polarity_scores(tw)
    pol_score['headline'] = tw
    results.append(pol_score)

# pprint(results[:3], width=100)
"""
Our dataframe consists of four columns from the sentiment scoring:
Neu, Neg, Pos and compound. The first three represent the sentiment score
percentage of each category in our headline, and the compound single number
that scores the sentiment. `compound` ranges from -1 (Extremely Negative) to
1 (Extremely Positive).
"""
df = pd.DataFrame.from_records(results)
print(df.head())

# Plotting distribution
#fig, axs = plt.subplots(tight_layout=True)
# We can set the number of bins with the `bins` kwarg
#axs.hist(x, bins=n_bins)
"""
tweets_by_score = df['compound'].value_counts(normalize=True) * 100
fig, ax = plt.subplots()
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('Score', fontsize=15)
ax.set_ylabel('Number of tweets' , fontsize=15)
ax.set_title('SIA', fontsize=15, fontweight='bold')
tweets_by_score.plot(ax=ax, kind='bar', color='blue')
plt.show()
"""
# https://medium.com/free-code-camp/how-to-make-your-own-sentiment-analyzer-using-python-and-googles-natural-language-api-9e91e1c493e
# Using Google’s score range, as we see in the image below.
# NEG = -1.0 - -0.25
# NEU = -0.25 - 0.25
# POS = 0.25 - 1.0
# Let's create the labels

df['label'] = 0
df.loc[ (df['compound'] >= -1.0) & (df['compound'] <= -0.25), 'label'] = -1 # neg
df.loc[ (df['compound'] >= -0.25) & (df['compound'] <= 0.25), 'label'] = 0 # neutral
df.loc[ (df['compound'] >= 0.25) & (df['compound'] <= 1.0), 'label'] = 1 # POS

print(df.head())
print('MÉDIA DE SENTIMENTO: ' + str(np.mean(df['label'])))

# Plotting
"""
fig, ax = plt.subplots(figsize=(8, 8))
counts = df.label.value_counts(normalize=True) * 100
sns.barplot(x=counts.index, y=counts, ax=ax)
ax.set_xticklabels(['Negative', 'Neutral', 'Positive'])
ax.set_ylabel("Percentage")
plt.show()
"""
