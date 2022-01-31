import os
import unidecode

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from config import *

# Load corpus and query
df_corpus = pd.read_csv(os.path.join(DATASET_DIR, 'corpus.csv'))
df_query = pd.read_csv(os.path.join(DATASET_DIR, 'query.csv'))

# Create Td-idf model & embed documents
model_text = TfidfVectorizer(stop_words='english', binary=True, max_features=25_000)
embeddings_corpus = model_text.fit_transform(df_corpus.title).toarray()

# Query embedding
query = df_query.iloc[:]
embeddings_query = model_text.transform(query.title).toarray()

# Matrix multiplication to compute cosine similarity
cosine_similarity = np.transpose(embeddings_corpus @ embeddings_query.T)

# Output results
results = []
for group in cosine_similarity:
    matched_index = np.where(group >= TFIDF_THRESHOLD)
    matched_list = df_corpus.iloc[matched_index[0]]['posting_id'].to_list()
    results.append(matched_list)
print(results)