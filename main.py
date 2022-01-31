import os

import pandas as pd

from tfidf import TFIDF
from config import *

# Load corpus and query
df_corpus = pd.read_csv(os.path.join(DATASET_DIR, 'corpus.csv'))
df_query = pd.read_csv(os.path.join(DATASET_DIR, 'query.csv'))

# Create TF-IDF model
tfidf = TFIDF(df_corpus)

results = tfidf.query(df_query)
print(results)