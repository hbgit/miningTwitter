import json
import pandas as pd
import matplotlib.pyplot as plt

tweets_data_path = 'twitter_data.json'

tweets_data = []
# reading the JSON data using json.load()
with open(tweets_data_path, 'r') as f:
    for line in f:
        tweet = json.loads(line)
        tweets_data.append(tweet)


# converting json dataset from dictionary to dataframe
tweets = pd.DataFrame(tweets_data)
print(tweets.head())

"""
print("Plotting Languages ...")
tweets_by_lang = tweets['lang'].value_counts()
fig, ax = plt.subplots()
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('Languages', fontsize=15)
ax.set_ylabel('Number of tweets', fontsize=15)
ax.set_title('Top 5 languages', fontsize=15, fontweight='bold')
tweets_by_lang[:5].plot(ax=ax, kind='bar', color='red')
fig.savefig('languages.png')   # save the figure to file
plt.close(fig)
"""


print("Plotting by country ...")

tweets_place = pd.DataFrame([place for place in tweets['place'] if place is not None])
tweets_by_country = tweets_place['country']
print(tweets_by_country.value_counts())

tweets_by_country_top_five = tweets_by_country.value_counts()[:5]

fig, ax = plt.subplots()
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('Countries', fontsize=15)
ax.set_ylabel('Number of tweets' , fontsize=15)
ax.set_title('Top 5 countries', fontsize=15, fontweight='bold')
tweets_by_country_top_five.plot(ax=ax, kind='bar', color='blue')
fig.savefig('country.png')   # save the figure to file
plt.close(fig)
