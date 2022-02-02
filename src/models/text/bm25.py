import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from rank_bm25 import BM25Okapi

from models.model import Model
from config import *

class BM25(Model):

    def __init__(self, df_corpus, topk=50):
        self.df_corpus = df_corpus
        self.topk = topk
        tokenized_corpus = df_corpus['title'].apply(lambda s: s.split()).to_list()
        self.model = BM25Okapi(tokenized_corpus)

    def query(self, df_query):
        tokenized_query = df_query['title'].apply(lambda s: s.split()).to_list()

        # Output results
        results = {}
        for (_, query), group in zip(df_query.iterrows(), tokenized_query):
            matched_index = [list(reversed(np.argsort(self.model.get_scores(group))))[:self.topk]]
            matched_list = self.df_corpus.iloc[matched_index[0]].posting_id.to_list()
            results[query.posting_id] = matched_list

        return results