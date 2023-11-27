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
before = time.time()
embeddings = model.embedding(abstracts)
db.add(abstracts, embeddings)
print(time.time() - before)
