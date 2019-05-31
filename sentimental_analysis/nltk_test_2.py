# Based on https://www.datacamp.com/community/tutorials/text-analytics-beginners-nltk

from nltk import pos_tag
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
import matplotlib.pyplot as plt
from nltk.corpus import stopwords

# Stemming
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

#Lexicon Normalization
#performing stemming and Lemmatization
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer

text="""Hello Mr. Smith, how are you doing today? The weather is great, and city is awesome.
The sky is pinkish-blue. You shouldn't eat cardboard"""

tokenized_text=sent_tokenize(text)
print(tokenized_text)

print()
tokenized_word=word_tokenize(text)
print(tokenized_word)

fdist = FreqDist(tokenized_word)
print()
print(fdist)
print(fdist.most_common(2))

print()
#fdist.plot(30,cumulative=False)
#plt.show()

stop_words=set(stopwords.words("english"))
#print(stop_words)
# Removing Stopwords
filtered_sent=[]
for w in tokenized_word:
    if w not in stop_words:
        filtered_sent.append(w)

print("Tokenized Sentence:",tokenized_word)
print("Filterd Sentence:",filtered_sent)

# Stemming
# Stemming is a process of linguistic normalization, which reduces words to
# their word root word or chops off the derivational affixes.
ps = PorterStemmer()

stemmed_words=[]
for w in filtered_sent:
    stemmed_words.append(ps.stem(w))

print("Filtered Sentence:",filtered_sent)
print("Stemmed Sentence:",stemmed_words)

# Lemmatization reduces words to their base word, which is linguistically correct lemmas
lem = WordNetLemmatizer()
stem = PorterStemmer()

word = "flying"
print()
print("Lemmatized Word:",lem.lemmatize(word,"v"))
print("Stemmed Word:",stem.stem(word))

# POS Tagging
sent = "Albert Einstein was born in Ulm, Germany in 1879."
tokens = word_tokenize(sent)
print()
print(tokens)
print(pos_tag(tokens))

# Machine learning based approach - Sentiment Analysis
# sentiment-analysis-on-movie-reviews
print()
import pandas as pd
data=pd.read_csv('sentiment-analysis-on-movie-reviews/train.tsv', sep='\t')
print(data.head())
print(data.info())
print(data.Sentiment.value_counts())

"""
Sentiment_count=data.groupby('Sentiment').count()
plt.bar(Sentiment_count.index.values, Sentiment_count['Phrase'])
plt.xlabel('Review Sentiments')
plt.ylabel('Number of Review')
plt.show()
"""

# Feature Generation using Bag of Words
from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize import RegexpTokenizer
#tokenizer to remove unwanted elements from out data like symbols and numbers
token = RegexpTokenizer(r'[a-zA-Z0-9]+')
cv = CountVectorizer(lowercase=True,stop_words='english',ngram_range = (1,1),tokenizer = token.tokenize)
text_counts = cv.fit_transform(data['Phrase'])
# print(text_counts)

# Split train and test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    text_counts, data['Sentiment'], test_size=0.3, random_state=1)

# Model Building and Evaluation
# Let's build the Text Classification Model using TF-IDF
from sklearn.naive_bayes import MultinomialNB
#Import scikit-learn metrics module for accuracy calculation
from sklearn import metrics
# Model Generation Using Multinomial Naive Bayes
clf = MultinomialNB().fit(X_train, y_train)
predicted= clf.predict(X_test)
print("MultinomialNB Accuracy:",metrics.accuracy_score(y_test, predicted))

# Feature Generation using TF-IDF
# IDF(Inverse Document Frequency) measures the amount of information a given word provides across the document.
from sklearn.feature_extraction.text import TfidfVectorizer
tf=TfidfVectorizer()
text_tf= tf.fit_transform(data['Phrase'])

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    text_tf, data['Sentiment'], test_size=0.3, random_state=123)

from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
# Model Generation Using Multinomial Naive Bayes
clf = MultinomialNB().fit(X_train, y_train)
predicted= clf.predict(X_test)
print("MultinomialNB Accuracy:",metrics.accuracy_score(y_test, predicted))
