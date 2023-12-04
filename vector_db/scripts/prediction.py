import argparse
from pathlib import Path

import pandas as pd

from vector_db.app.database import DataBase
from vector_db.app.model import Model

parser = argparse.ArgumentParser()
parser.add_argument('--path-to-target', type=Path)
parser.add_argument('--path-to-full', type=Path)
args = parser.parse_args()

model = Model()

settings = {
    "name":"arxiv"
}
db = DataBase(settings)

df_google = pd.read_csv(args.path_to_target)
df_google = df_google.dropna()

df_full = pd.read_csv(args.path_to_full)


columns = ['query_article_link']
for i in range(1, 11):
    columns.append(f'top{i}')
df = pd.DataFrame(columns=columns)

for row in df_google['query_article_link']:
    full_row = df_full.loc[df_full['_url'] == row]
    abstract = full_row['_abstract'].str.replace('Abstract:', '').values[0]
    embedding = model.embedding(abstract)
    results = db.query_embedding(embedding)

    df.loc[len(df)] = [full_row['_url'].values[0]] + [item['url'] for item in results['metadatas'][0]]

df.to_csv('result.csv')

    