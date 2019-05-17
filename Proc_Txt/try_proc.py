from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import wordnet
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords
import re

from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd

#  Sentence Tokenization
text = "Backgammon is one of the oldest known board games. Its history can be \
traced back nearly 5,000 years to archeological discoveries in the Middle East.\
 It is a two player game where each player has fifteen checkers which move \
 between twenty-four points according to the roll of two dice."

sentences = nltk.sent_tokenize(text)
for sentence in sentences:
    print(sentence)
    print()

#  Word Tokenization
for sentence in sentences:
    words = nltk.word_tokenize(sentence)
    print(words)
    print()


#  Text Lemmatization and Stemming
def compare_stemmer_and_lemmatizer(stemmer, lemmatizer, word, pos):
    """
    Print the results of stemmind and lemmitization using the passed stemmer, \
    lemmatizer, word and pos (part of speech)
    """
    print("Stemmer:", stemmer.stem(word))
    print("Lemmatizer:", lemmatizer.lemmatize(word, pos))
    print()


lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()
compare_stemmer_and_lemmatizer(
    stemmer, lemmatizer, word="seen", pos=wordnet.VERB)
compare_stemmer_and_lemmatizer(
    stemmer, lemmatizer, word="drove", pos=wordnet.VERB)


#  Stop words
print(stopwords.words("portuguese"))

stop_words = set(stopwords.words("portuguese"))
sentence = "Os meninos estão correndo do cachorro."

words = nltk.word_tokenize(sentence)
without_stop_words = [word for word in words if not word in stop_words]
print(without_stop_words)


#  Regex
sentence = "The development of snowboarding was inspired by skateboarding, sledding, surfing and skiing."
pattern = r"[^\w]"
print(re.sub(pattern, " ", sentence))


#  Bag-of-words
#  It is a popular and simple feature extraction technique
with open("text.txt", "r") as file:
    documents = file.read().splitlines()

print(documents)

#  Step 2. Design the Vocabulary
#  The default token pattern removes tokens of a single character. That's why we
#  don't have the "I" and "s" tokens in the output
count_vectorizer = CountVectorizer()

#  Step 3. Create the Bag-of-Words Model
bag_of_words = count_vectorizer.fit_transform(documents)

#  Show the Bag-of-Words Model as a pandas DataFrame
feature_names = count_vectorizer.get_feature_names()
print(pd.DataFrame(bag_of_words.toarray(), columns=feature_names))

#  frequent across all the documents

tfidf_vectorizer = TfidfVectorizer()
values = tfidf_vectorizer.fit_transform(documents)

# Show the Model as a pandas DataFrame
feature_names = tfidf_vectorizer.get_feature_names()
print(pd.DataFrame(values.toarray(), columns=feature_names))
