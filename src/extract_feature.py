import os
import cv2
import numpy as np
import pandas as pd
import time
import tqdm
from datetime import timedelta
from scipy.cluster.vq import kmeans, vq
from sklearn.preprocessing import normalize
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.cluster import KMeans, MiniBatchKMeans

import config

df_corpus = pd.read_csv(os.path.join(config.DATASET_DIR, 'corpus.csv'))
img_list = df_corpus['image'].unique()
img_list.sort()

def compute_features(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    sift = cv2.SIFT_create()
    kps, des = sift.detectAndCompute(img_gray, None)

    featvect = des
    return featvect 

def extract_sift(img_list):
    # List of features that stores
    feat = []

    start_time = time.time()
    print('Extracting SIFT feature...')
    for img_name in tqdm.tqdm(img_list):
        img_path = os.path.join(config.DATASET_DIR, 'train_images', img_name)
        # Load and convert image
        img = cv2.imread(img_path)

        # Compute SIFT features for each keypoints
        feat.append(compute_features(img))
    end_time = time.time()

    print('Extracted SIFT feature in', str(timedelta(seconds=(end_time-start_time))))

    np.savez_compressed(os.path.join(config.DATASET_DIR, 'sift.npz'), feat=feat)

    return feat

def generate_codebook(feat, k=50):
    # Stack all features together
    alldes = np.vstack(feat)

    # Perform K-means clustering
    alldes = np.float32(alldes)      # convert to float, required by kmeans and vq functions
    start_time = time.time()
    # codebook, distortion = kmeans(alldes, k)
    codebook = MiniBatchKMeans(n_clusters=k, random_state=42, batch_size=k*4, verbose=True).fit(alldes).cluster_centers_
    end_time = time.time()
    print('kmeans', end_time - start_time)
    # code, distortion = vq(alldes, codebook)
    end_time = time.time()
    print("Built {}-cluster codebook from {} feature vectors in {}".format(
        k,
        alldes.shape[0],
        str(timedelta(seconds=(end_time-start_time))),
    ))

    np.savez_compressed(os.path.join(config.DATASET_DIR, 'sift_codebook.npz'), codebook=codebook)
    return codebook

def extract_bow(codebook, feat, k=50):
    #====================================================================
    # Bag-of-word Features
    #====================================================================
    # Create Bag-of-word list
    bow = []
    
    # Get label for each image, and put into a histogram (BoW)
    for f in tqdm.tqdm(feat):
        code, distortion = vq(f, codebook)
        bow_hist, _ = np.histogram(code, k, density=True)
        bow.append(bow_hist)
    
    # Stack them together
    temparr = np.vstack(bow)
    
    # Put them into feature vector
    feat = np.reshape(temparr, (temparr.shape[0], temparr.shape[1]) )
    
    np.savez_compressed(os.path.join(config.DATASET_DIR, 'sift_bow.npz'), feat=feat)
    
    return feat, bow

def extract_tfidf(codebook, feat, k=50):
    #====================================================================
    # TF-IDF Features
    #====================================================================
    def tfidf(bow):
        # td-idf weighting
        transformer = TfidfTransformer(smooth_idf=True)
        t = transformer.fit_transform(bow).toarray()
        
        # normalize by Euclidean (L2) norm before returning 
        t = normalize(t, norm='l2', axis=1)
        
        return t
    
    bow = []
    
    # Get label for each image, and put into a histogram (BoW)
    for f in tqdm.tqdm(feat):
        code, distortion = vq(f, codebook)
        bow_hist, _ = np.histogram(code, k)
        bow.append(bow_hist)
    
    # re-run vq without normalization, normalize after computing tf-idf
    bow = np.vstack(bow)
    t = tfidf(bow)
    np.savez_compressed(os.path.join(config.DATASET_DIR, 'sift_bow_raw.npz'), feat=bow)
    
    return bow, t


if __name__ == '__main__':
    feat = np.load(os.path.join(config.DATASET_DIR, 'backup', 'sift.npz'), allow_pickle=True)['feat']
    codebook = np.load(os.path.join(config.DATASET_DIR, 'backup', 'sift_codebook.npz'), allow_pickle=True)['codebook']
    print('ok')
    codebook = generate_codebook(feat, k=config.SIFT_CODEBOOK_SIZE)
    extract_bow(codebook, feat, k=config.SIFT_CODEBOOK_SIZE)
    extract_tfidf(codebook, feat, k=config.SIFT_CODEBOOK_SIZE)