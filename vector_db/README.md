# vector-db-servie

## Running locally

1. Change current directory: `cd vector_db` 
2. Run server
```bash
uvicorn app.main:app --reload
```

## Results

| Model                      | Metric | Accuracy |
| -------------------------- | ------ | -------- |
| all-MiniLM-L6-v2           | Cosin  | 0.013    |
| all-mpnet-base-v2          | Cosin  |          |
| all-distilroberta-v1       | Cosin  |          |
| multi-qa-distilbert-cos-v1 | Cosin  |          |

