import os

import pandas as pd
import numpy as np

from models.text.tfidf import TFIDF
from models.text.bm25 import BM25
from models.image.sift import SIFT
from models.model import Model
from utils.evaluate import EvaluateMAP
from config import *

if __name__ == '__main__':
    # Load corpus and query
    df_corpus = pd.read_csv(os.path.join(DATASET_DIR, 'corpus.csv'))
    df_query = pd.read_csv(os.path.join(DATASET_DIR, 'query.csv'))

    evaluate_map = EvaluateMAP(df_corpus, df_query)

    sift = SIFT(df_corpus, tfidf=False)
    print('loaded sift')
    for threshold in np.arange(0.5, 1, 0.05):
        pred = sift.query(df_query.iloc[:10], threshold=threshold)
        print(threshold, evaluate_map(pred))

    # bm25 = BM25(df_corpus)
    # pred = bm25.query(df_query)
    # print(evaluate_map(pred))

    # for threshold in range(1, 10):
    #     # Create TF-IDF model
    #     tfidf = TFIDF(df_corpus, threshold=threshold/10)

    #     pred = tfidf.query(df_query)

    #     print(threshold/10, evaluate_map(pred))