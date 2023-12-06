# vector-db-servie

## Running locally

1. Change current directory: `cd vector_db` 
2. Run server
```bash
uvicorn app.main:app --reload
```

## Results
- All targets samples: 590
- Broken samples: 153
- Unrelated samples: 220
- Target samples: 217

### L2 abstract
| Model                      | Precisions | Top-K |
| -------------------------- | ---------- | ----- |
| all-MiniLM-L6-v2           | 0.12       | 1.16  |
| all-mpnet-base-v2          |            |       |
| all-distilroberta-v1       |            |       |
| multi-qa-distilbert-cos-v1 |            |       |
| e5-large                   |            |       |

### L2 title
| Model                      | Precisions | Top-K |
| -------------------------- | ---------- | ----- |
| all-MiniLM-L6-v2           | 0.11       | 1.10  |
| all-mpnet-base-v2          |            |       |
| all-distilroberta-v1       |            |       |
| multi-qa-distilbert-cos-v1 |            |       |
| e5-large                   |            |       |
