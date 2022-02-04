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

feat = extract_sift(img_list)

raise Exception()

def generate_codebook(feat, k=50):
    # Stack all features together
    alldes = np.vstack(feat)

    # Perform K-means clustering
    alldes = np.float32(alldes)      # convert to float, required by kmeans and vq functions
    start_time = time.time()
    codebook, distortion = kmeans(alldes, k)
    code, distortion = vq(alldes, codebook)
    end_time = time.time()
    print("Built {}-cluster codebook from {} images in {}".format(
        k,
        alldes.shape[0],
        str(timedelta(seconds=(end_time-start_time))),
    ))

    # Save codebook as pickle file
    pickle.dump(codebook, open("codebook.pkl", "wb"))

    return codebook

feat = np.load(os.path.join(config.DATASET_DIR, 'sift.npy'))
generate_codebook()

# Load cookbook
codebook = pickle.load(open("codebook.pkl", "rb"))

##############################################################################

# these labels are the classes assigned to the actual plant names
labels = ('C1','C2','C3','C4','C5','C6','C7','C8','C9','C10')     # BUG FIX 1: changed class label from integer to string


#====================================================================
# Bag-of-word Features
#====================================================================
# Create Bag-of-word list
bow = []

# Get label for each image, and put into a histogram (BoW)
for f in feat:
    code, distortion = vq(f, codebook)
    bow_hist, _ = np.histogram(code, k, normed=True)
    bow.append(bow_hist)
    
# Stack them together
temparr = np.vstack(bow)

# Put them into feature vector
fv = np.reshape(temparr, (temparr.shape[0], temparr.shape[1]) )
del temparr


# pickle your features (bow)
pickle.dump(fv, open("bow.pkl", "wb"))
print('')
print('Bag-of-words features pickled!')

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

# re-run vq without normalization, normalize after computing tf-idf
bow = np.vstack(bow)
t = tfidf(bow)

# pickle your features (tfidf)
pickle.dump(t, open("tfidf.pkl", "wb"))
print('TF-IDF features pickled!')

#====================================================================
# Baseline Features
#====================================================================
# Stack all features together
base_feat = np.vstack(base_feat)

# pickle your features (baseline)
pickle.dump(base_feat, open("base.pkl", "wb"))
print('Baseline features pickled!')

#====================================================================
