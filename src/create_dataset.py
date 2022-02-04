import os
import re

import pandas as pd

from config import *

df_path = os.path.join(DATASET_DIR, 'train.csv')

# Load data
df = pd.read_csv(df_path)

print('Loading dataset from', df_path)
print('Found', len(df['label_group'].unique()), 'label groups.')

# Filter groups with at least 10 elements
df = df[df.label_group.isin(
    df.groupby('label_group').count().query('posting_id >= 5').index
)]

print(f'Found {len(df["label_group"].unique())} groups ({len(df)} items) with at least 5 elements.')
print('Sampling query set...')

# Remove \xHH characters from title
df['title'] = df['title'].apply(lambda s: re.sub('\\\\x\w\w', '', s))
# Remove special characters from title
df['title'] = df['title'].apply(lambda s: re.sub('[^\w]+', ' ', s))
# Remove unneccessary whitespaces
df['title'] = df['title'].apply(lambda s: re.sub('  ', ' ', s))
df['title'] = df['title'].apply(lambda s: re.sub('^ ', '', s))
df['title'] = df['title'].apply(lambda s: re.sub(' $', '', s))
# Convert to lowercase
df['title'] = df['title'].apply(lambda s: s.lower())

# Sample 2 elements from each group for query set
sample_list = df.groupby('label_group').sample(n=1, random_state=42).posting_id
df_query = df[df.posting_id.isin(sample_list)]
# Subtract query set to obtain the remaining part (corpus)
df_corpus = pd.concat([df, df_query]).drop_duplicates(keep=False)

# Save csv files
df_corpus.reset_index(drop=True).to_csv(os.path.join(DATASET_DIR, 'corpus.csv'))
df_query.reset_index(drop=True).to_csv(os.path.join(DATASET_DIR, 'query.csv'))

print('Saved corpus and query set to', DATASET_DIR)