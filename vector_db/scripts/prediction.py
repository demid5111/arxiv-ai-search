import argparse
import random
import statistics
from pathlib import Path

import pandas as pd
from sklearn.metrics import accuracy_score

from vector_db.app.database import DataBase
from vector_db.app.model import Model

parser = argparse.ArgumentParser()
parser.add_argument('--path-to-target', type=Path)
parser.add_argument('--path-to-full', type=Path)
parser.add_argument('--random', type=bool)
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

accuracy = []
precisions = []
all_tp = 0
unrelated = 0

if args.random:
    predicts = [df_google.iloc[[random.randint(
        0, len(df_google) - 1)]].values[0][2:].tolist()[random.randint(0, 9)] for _ in range(10)]


for row in df_google.iterrows():
    tp = 0
    fp = 0
    top_k_flag = True

    break_flag = 0
    targets = row[1][1:-1].to_list()

    for item in targets:
        find = df_full.loc[df_full['_url'] == item]
        if len(find) == 0:
            unrelated += 1
            break_flag += 1
            break
    if break_flag:
        continue

    full_row = df_full.loc[df_full['_url'] == row[1]['query_article_link']]
    if not args.random:
        # text = full_row['_abstract'].str.replace('Abstract:', '').values[0]
        text = full_row['_title'].values[0]
        embedding = model.embedding(text)
        results = db.query_embedding(embedding)

        predicts = [item['url'] for item in results['metadatas'][0]]
        df.loc[len(df)] = [full_row['_url'].values[0]]+[item['url']
                                                        for item in results['metadatas'][0]]
    accuracy.append((targets[0], predicts[0]))
    for item in targets:
        if item in predicts:
            if top_k_flag:
                all_tp += 1
                top_k_flag = False
            tp += 1
        else:
            fp += 1
    precision = tp / (tp + fp)
    precisions.append(precision)
samples = len(df_google) - unrelated
# df.to_csv('result_all-distilroberta-v1_cosine_.csv')

print('Top-1: ', accuracy_score(
    [item[0] for item in accuracy],
    [item[1] for item in accuracy])
)
print('Unrelated samples: ', unrelated)
print('Target samples: ', samples)
print('Precisions: ', statistics.mean(precisions))
print('Top-K: ', all_tp / samples)
