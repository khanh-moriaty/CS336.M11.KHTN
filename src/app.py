import os
import time

import pandas as pd
from flask import Flask, request

from tfidf import TFIDF
from bm25 import BM25
from evaluate import EvaluateMAP
from config import *

app = Flask(__name__)

@app.route("/v1/query")
def query():
    text = request.args.get('text', default='')
    image = request.args.get('image', default='')
    model_text = request.args.get('model_text', default='')
    model_image = request.args.get('model_image', default='')
    response = {
        'text': text,
        'image': image,
        'model_text': model_text,
        'model_image': model_image,
        'processing_time': 0,
        'results': {}
    }

    start_time = time.time()

    if text and model_text in ['tfidf', 'bm25']:
        pass

    if image and model_image in ['sift']:
        pass

    end_time = time.time()
    response['processing_time'] = end_time - start_time

    return results