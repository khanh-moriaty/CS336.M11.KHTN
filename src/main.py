import os

import pandas as pd

from tfidf import TFIDF
from bm25 import BM25
from evaluate import EvaluateMAP
from config import *

# Load corpus and query
df_corpus = pd.read_csv(os.path.join(DATASET_DIR, 'corpus.csv'))
df_query = pd.read_csv(os.path.join(DATASET_DIR, 'query.csv'))

evaluate_map = EvaluateMAP(df_corpus, df_query)

# bm25 = BM25(df_corpus)
# pred = bm25.query(df_query)
# print(evaluate_map(pred))

for threshold in range(1, 10):
    # Create TF-IDF model
    tfidf = TFIDF(df_corpus, threshold=threshold/10)

    pred = tfidf.query(df_query)

    print(threshold/10, evaluate_map(pred))