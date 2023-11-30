import argparse
import time
from pathlib import Path

import pandas as pd

from vector_db.app.database import DataBase
from vector_db.app.model import Model

parser = argparse.ArgumentParser()
parser.add_argument('--path', type=Path)
args = parser.parse_args()

model = Model()
settings = {
    "name":"arxiv"
}
db = DataBase(settings)

# 566847
filename = args.path
df = pd.read_csv(filename)
abstracts = []
abstracts = df['_abstract'].str.replace('Abstract:', '').to_list()
chunk_size = 10000

abstracts_len = len(abstracts)
for index in range(abstracts_len % chunk_size):
    before = time.time()
    start_slice = index * chunk_size
    end_slice = start_slice + chunk_size

    if end_slice >= abstracts_len:
        abstracts_chunk = abstracts[start_slice:]
    else:
        abstracts_chunk = abstracts[start_slice:end_slice]
    embeddings = model.embedding(abstracts_chunk)
    db.add(abstracts_chunk, embeddings)
    print(f'Iteratin {index}, time: ',time.time() - before)
