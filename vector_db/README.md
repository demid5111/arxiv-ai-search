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
- Unrelated samples: 202
- Target samples: 235

### L2 abstract
| Model                      | Precisions | Top-K     |
| -------------------------- | ---------- | --------- |
| all-MiniLM-L6-v2           | 0.21148    | 2.114893  |
| all-mpnet-base-v2          | 0.215319   | 2.153191  |
| all-distilroberta-v1       | 0.21787    | 2.178723  |
| multi-qa-distilbert-cos-v1 | 0.1914893  | 1.9148936 |
| e5-large                   |            |           |

### L2 title
| Model                      | Precisions | Top-K    |
| -------------------------- | ---------- | -------- |
| all-MiniLM-L6-v2           | 0.17191    | 1.719148 |
| all-mpnet-base-v2          | 0.189361   | 1.893617 |
| all-distilroberta-v1       | 0.17489    | 1.748936 |
| multi-qa-distilbert-cos-v1 | 0.1446808  | 1.446808 |
| e5-large                   |            |          |


### Cosine abstract
| Model                      | Precisions | Top-K    |
| -------------------------- | ---------- | -------- |
| all-MiniLM-L6-v2           | 0.21148    | 2.114893 |
| all-mpnet-base-v2          | 0.21531    | 2.153191 |
| all-distilroberta-v1       | 0.21787    | 2.178723 |
| multi-qa-distilbert-cos-v1 | 0.191489   | 1.914893 |
| e5-large                   |            |          |

### Cosine title
| Model                      | Precisions | Top-K    |
| -------------------------- | ---------- | -------- |
| all-MiniLM-L6-v2           | 0.17191    | 1.719148 |
| all-mpnet-base-v2          | 0.189361   | 1.893617 |
| all-distilroberta-v1       | 0.17489    | 1.748936 |
| multi-qa-distilbert-cos-v1 | 0.144680   | 1.446808 |
| e5-large                   |            |          |