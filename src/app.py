import os
import time

import pandas as pd
from flask import Flask, request, send_file, url_for
from werkzeug.utils import secure_filename

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

evaluate_map = EvaluateMAP(df_corpus, df_query)

app = Flask(__name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

os.makedirs(config.UPLOAD_DIR, exist_ok=True)

def query_df(df_query, model_text, model_image):
    start_time = time.time()

    if model_text in ['tfidf', 'bm25']:
        results = models[model_text](df_query)

    if model_image in ['sift']:
        pass

    end_time = time.time()
    processing_time = end_time - start_time

    return results, processing_time

def get_img_path(img_name):
    img_path = os.path.join(config.DATASET_DIR, 'train_images', img_name)
    if os.path.exists(img_path):
        return img_path
    else:
        img_path = os.path.join(config.UPLOAD_DIR, img_name)
        if os.path.exists(img_path):
            return img_path
        else:
            return None

@app.route("/v1/img/<img_name>")
def fetch_img(img_name):
    img_path = get_img_path(img_name)
    if not img_path:
        return {'error': 'Image name not found.'}, 400
    return send_file(img_path, as_attachment=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/v1/upload", methods=["POST"])
def upload_img():
    # check if the post request has the file part
    if 'file' not in request.files:
        return 400
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        return 400
    if file and allowed_file(file.filename):
        filename = str(int(time.time())) + '_' + secure_filename(file.filename)
        file.save(os.path.join(config.UPLOAD_DIR, filename))
        print(url_for('fetch_img', img_name=filename))
        return {'image_path': url_for('fetch_img', img_name=filename)}

@app.route("/v1/exp")
def query_exp():
    model_text = request.args.get('model_text', default='')
    model_image = request.args.get('model_image', default='')

    results, processing_time = query_df(df_query, model_text, model_image)
    score = evaluate_map(results)

    return {
        'model_text': model_text,
        'model_image': model_image,
        'processing_time': processing_time,
        'score': score,
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

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5000, debug=True)