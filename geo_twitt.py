"""
Note:
cd greve_data
cat xaa  xab  xac  xad  xae  xaf  xag  xah  xai  xaj  xak  xal > greve.json
"""
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

geo_data = {
    "type": "FeatureCollection",
    "features": []
}

with open('greve_data/greve.json', 'r') as f:
    for line in f:
        tweet = json.loads(line)
        if tweet['coordinates']:
            geo_json_feature = {
                "type": "Feature",
                "geometry": tweet['coordinates'],
                "properties": {
                    "text": tweet['text'],
                    "created_at": tweet['created_at']
                }
            }
            geo_data['features'].append(geo_json_feature)

# Save geo data
with open('geo_data.json', 'w') as fout:
    fout.write(json.dumps(geo_data, indent=4))
