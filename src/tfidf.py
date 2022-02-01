import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from config import *

class TFIDF:

    def __init__(self, df_corpus, threshold=0.5):
        self.df_corpus = df_corpus
        self.threshold = threshold
        # Create Td-idf model & embed documents
        self.model_text = TfidfVectorizer(stop_words='english', binary=True, max_features=25_000)
        self.embeddings_corpus = self.model_text.fit_transform(df_corpus.title).toarray()

    def query(self, df_query):
        # Query embedding
        embeddings_query = self.model_text.transform(df_query.title).toarray()

        # Matrix multiplication to compute cosine similarity
        cosine_similarity = np.transpose(self.embeddings_corpus @ embeddings_query.T)

        # Output results
        results = {}
        for (_, query), group in zip(df_query.iterrows(), cosine_similarity):
            matched_index = np.where(group >= self.threshold)
            matched_list = self.df_corpus.iloc[matched_index[0]].posting_id.to_list()
            results[query.posting_id] = matched_list

        return results