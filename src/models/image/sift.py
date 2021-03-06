import os

import cv2
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer
from sklearn.preprocessing import normalize
from scipy.cluster.vq import vq

from models.model import Model
import config

class SIFT(Model):

    def __init__(self, df_corpus, tfidf=True):
        self.df_corpus = df_corpus
        self.tfidf = tfidf
        # Create Td-idf model & embed documents
        self.codebook = np.load(os.path.join(config.DATASET_DIR, 'sift_codebook.npz'), allow_pickle=True)['codebook']
        self.embeddings_corpus = np.load(os.path.join(config.DATASET_DIR, 'sift_bow_raw.npz'), allow_pickle=True)['feat']
        
        if tfidf:
            self.model = TfidfTransformer(smooth_idf=True)
            self.embeddings_corpus = self.model.fit_transform(self.embeddings_corpus).toarray()

        self.embeddings_corpus = normalize(self.embeddings_corpus, norm='l2', axis=1)

        self.img_list = df_corpus['image'].unique()
        self.img_list.sort()

    def compute_features(self, img):
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        sift = cv2.SIFT_create()
        kps, des = sift.detectAndCompute(img_gray, None)

        featvect = des
        return featvect 

    def query(self, df_query, threshold=0.5):
        embeddings_query = []
        query_img = df_query.image
        for img in query_img:
            img = cv2.imread(os.path.join(config.DATASET_DIR, 'train_images', img))
            feat = self.compute_features(img)
            code, distortion = vq(feat, self.codebook)
            bow_hist, _ = np.histogram(code, config.SIFT_CODEBOOK_SIZE)
            embeddings_query.append(bow_hist)

        if self.tfidf:
            embeddings_query = self.model.transform(embeddings_query).toarray()

        embeddings_query = normalize(embeddings_query, norm='l2', axis=1)

        # Matrix multiplication to compute cosine similarity
        cosine_similarity = np.transpose(self.embeddings_corpus @ embeddings_query.T)

        # Output results
        results = {}
        for (_, query), group in zip(df_query.iterrows(), cosine_similarity):
            matched_index = np.where(group >= threshold)
            matched_index = self.img_list[matched_index[0]]
            matched_list = self.df_corpus[self.df_corpus['image'].isin(matched_index)].posting_id.to_list()
            results[query.posting_id] = matched_list

        return results