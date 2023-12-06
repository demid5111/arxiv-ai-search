import argparse
import statistics
from pathlib import Path

import pandas as pd
from sklearn.metrics import precision_score

from vector_db.app.database import DataBase
from vector_db.app.model import Model

parser = argparse.ArgumentParser()
parser.add_argument('--path-to-target', type=Path)
parser.add_argument('--path-to-full', type=Path)
args = parser.parse_args()

model = Model()

settings = {
    "name": "arxiv"
}
db = DataBase(settings)

df_google = pd.read_csv(args.path_to_target)
print('All targets: ', len(df_google))

df_google = df_google.dropna()
print('After drop targets: ', len(df_google))

df_full = pd.read_csv(args.path_to_full)


columns = ['query_article_link']
for i in range(1, 11):
    columns.append(f'top{i}')
df = pd.DataFrame(columns=columns)

precisions = []
all_tp = 0
unrelated = 0

for row in df_google.iterrows():
    tp = 0
    fp = 0

    break_flag = 0
    targets = row[1][2:].to_list()

    for item in targets:
        find = df_full.loc[df_full['_url'] == item]
        if len(find) == 0:
            unrelated += 1
            break_flag += 1
            break
    if break_flag:
        continue

    full_row = df_full.loc[df_full['_url'] == row[1]['query_article_link']]
    # abstract = full_row['_abstract'].str.replace('Abstract:', '').values[0]
    abstract = full_row['_title'].values[0]
    embedding = model.embedding(abstract)
    results = db.query_embedding(embedding)

    predicts = [item['url'] for item in results['metadatas'][0]]
    for item in targets:
        if item in predicts:
            all_tp += 1
            tp += 1
        else:
            fp += 1
    precision = tp / (tp + fp)
    precisions.append(precision)
samples = len(df_google) - unrelated

print('Unrelated samples: ', unrelated)
print('Target samples: ', samples)
print('Precisions: ', statistics.mean(precisions))
print('Top-K: ', all_tp / samples)
