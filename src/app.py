import os
import time

import pandas as pd
from flask import Flask, request

from models.text.tfidf import TFIDF
from models.text.bm25 import BM25
from utils.evaluate import EvaluateMAP
import config

# Load corpus and query
df_corpus = pd.read_csv(os.path.join(config.DATASET_DIR, 'corpus.csv'))
df_query = pd.read_csv(os.path.join(config.DATASET_DIR, 'query.csv'))

models = {
    'tfidf': TFIDF(df_corpus, config.TFIDF_THRESHOLD)
}

app = Flask(__name__)

def query_df(df_query, model_text, model_image):
    start_time = time.time()

    if model_text in ['tfidf', 'bm25']:
        results = models[model_text](df_query)

    if model_image in ['sift']:
        pass

    end_time = time.time()
    processing_time = end_time - start_time

    return results, processing_time

@app.route("/v1/exp")
def query_exp():
    model_text = request.args.get('model_text', default='')
    model_image = request.args.get('model_image', default='')

    results, processing_time = query_df(df_query, model_text, model_image)

    return {
        'model_text': model_text,
        'model_image': model_image,
        'processing_time': processing_time,
        'results': results,
    }

@app.route("/v1/query")
def query():
    text = request.args.get('text', default='')
    image = request.args.get('image', default='')
    model_text = request.args.get('model_text', default='')
    model_image = request.args.get('model_image', default='')

    df_query = pd.DataFrame(data={
        'title': [text], 
        'image': [image], 
        'posting_id': [''], 
        'image_phash': [''], 
        'label_group': [0]
    })

    results, processing_time = query_df(df_query, model_text, model_image)

    return {
        'text': text,
        'image': image,
        'model_text': model_text,
        'model_image': model_image,
        'processing_time': processing_time,
        'results': results[''],
    }