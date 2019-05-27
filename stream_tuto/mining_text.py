import json
import pandas as pd
import re
import matplotlib.pyplot as plt

def word_in_text(word, text):
    word = word.lower()
    text = text.lower()
    match = re.search(word, text)
    if match:
        return True
    return False

tweets_data_path = 'twitter_data.json'

tweets_data = []
# reading the JSON data using json.load()
with open(tweets_data_path, 'r') as f:
    for line in f:
        tweet = json.loads(line)
        tweets_data.append(tweet)


# converting json dataset from dictionary to dataframe
tweets = pd.DataFrame(tweets_data)
# print(tweets.head())

tweets_python = pd.DataFrame([t for t in tweets['text'] if word_in_text('python', t)])
tweets_python.columns = ['text']
tweets_js = pd.DataFrame([t for t in tweets['text'] if word_in_text('javascript', t)])
tweets_js.columns = ['text']
tweets_ruby = pd.DataFrame([t for t in tweets['text'] if word_in_text('ruby', t)])
tweets_ruby.columns = ['text']

prg_langs = ['python', 'javascript', 'ruby']

tweets_by_prg_lang = [tweets_python['text'].value_counts()[True], tweets_js['text'].value_counts()[True], tweets_ruby['text'].value_counts()[True]]
print(tweets_by_prg_lang)

x_pos = list(range(len(prg_langs)))
width = 0.8
fig, ax = plt.subplots()
plt.bar(x_pos, tweets_by_prg_lang, width, alpha=1, color='g')

# Setting axis labels and ticks
ax.set_ylabel('Number of tweets', fontsize=15)
ax.set_title('Ranking: python vs. javascript vs. ruby (Raw data)', fontsize=10, fontweight='bold')
ax.set_xticks([p + 0.4 * width for p in x_pos])
ax.set_xticklabels(prg_langs)
plt.grid()
fig.savefig('langvs.png')   # save the figure to file
plt.close(fig)

# Targeting relevant tweets
tweets_prog = pd.DataFrame([t for t in tweets['text'] if word_in_text('programming', t)])
tweets_prog.columns = ['text']
tweets_tuto = pd.DataFrame([t for t in tweets['text'] if word_in_text('tutorial', t)])
tweets_tuto.columns = ['text']
tweets_relevant = pd.DataFrame([t for t in tweets['text'] if (word_in_text('tutorial', t)) or (word_in_text('programming', t)) ])
tweets_relevant.columns = ['text']

tweets_by_prg_lang_rele = [tweets_prog['text'].value_counts()[True],
                           tweets_tuto['text'].value_counts()[True],
                           tweets_relevant['text'].value_counts()[True]]

print(tweets_by_prg_lang_rele)

x_pos = list(range(len(prg_langs)))
width = 0.8
fig, ax = plt.subplots()
plt.bar(x_pos, tweets_by_prg_lang_rele, width,alpha=1,color='g')
ax.set_ylabel('Number of tweets', fontsize=15)
ax.set_title('Ranking: python vs. javascript vs. ruby (Relevant data)', fontsize=10, fontweight='bold')
ax.set_xticks([p + 0.4 * width for p in x_pos])
ax.set_xticklabels(prg_langs)
plt.grid()
fig.savefig('langRelevant.png')   # save the figure to file
plt.close(fig)
