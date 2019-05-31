#https://medium.com/@viniljf/criando-um-analisador-de-sentimentos-para-tweets-a53bae0c5147
import json
import pandas as pd
from textblob import TextBlob

tweets_data_path = '../greve_data/xaa'

tweets_data = []
# reading the JSON data using json.load()
with open(tweets_data_path, 'r') as f:
    for line in f:
        tweet = json.loads(line)
        tweets_data.append(tweet)

# converting json dataset from dictionary to dataframe
tweets = pd.DataFrame(tweets_data)
for tw in tweets['text']:
    print(tw)
    frase = TextBlob(tw)
    if frase.detect_language() != 'en':
        traducao = TextBlob(str(frase.translate(from_lang='pt', to='en')))
        print('Tweet: {0} - Sentimento: {1}'.format(tw, traducao.sentiment))
    else:
        print('Tweet: {0} - Sentimento: {1}'.format(tw, frase.sentiment))

"""
-POLARITY - é um valor contínuo que varia de -1.0 a 1.0, sendo -1.0
referente a 100% negativo e 1.0 a 100% positivo.

-SUBJECTIVITY - que também é um valor contínuo que varia de 0.0 a 1.0,
sendo 0.0 referente a 100% objetivo e 1.0 a 100% subjetivo.
"""
