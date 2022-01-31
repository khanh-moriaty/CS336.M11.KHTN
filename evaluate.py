import os

import pandas as pd
import numpy as np

from config import *

class EvaluateMAP:

    def __init__(self, df_corpus, df_query):
        # df_corpus['posting_id'] = df_corpus.groupby('label_group')['posting_id'].apply(list)
        df_corpus = df_corpus.groupby('label_group')
        df_corpus = pd.DataFrame(df_corpus['posting_id'].apply(list))
        self.gt = df_query.merge(df_corpus, on='label_group', how='left')
        self.gt = self.gt.rename(columns={'posting_id_x': 'posting_id', 'posting_id_y': 'results'})
        self.gt = self.gt.set_index('posting_id')[['results']]
        pass

    def __call__(self, pred):
        score = 0

        mAP = 0
        for posting_id, results in pred.items():
            gt = self.gt.query(f"posting_id == '{posting_id}'").iloc[0]['results']
            AP = np.zeros((len(gt),))
            TP = 0
            for i, res in enumerate(results):
                if res in gt:
                    j = gt.index(res)
                    TP += 1
                    AP[j] = TP/(i+1)
            AP = sum(AP) / len(AP)
            mAP += AP
        mAP /= len(pred)

        return mAP