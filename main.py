import os

import pandas as pd

from tfidf import TFIDF
from evaluate import EvaluateMAP
from config import *

# Load corpus and query
df_corpus = pd.read_csv(os.path.join(DATASET_DIR, 'corpus.csv'))
df_query = pd.read_csv(os.path.join(DATASET_DIR, 'query.csv'))

for threshold in range(1, 10):
    # Create TF-IDF model
    tfidf = TFIDF(df_corpus, threshold=threshold/10)

    results = tfidf.query(df_query)

    evaluate_map = EvaluateMAP(df_corpus, df_query)
    print(threshold/10, evaluate_map(results))