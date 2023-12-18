# vector-db-servie

## Running locally

1. Change current directory: `cd vector_db` 
2. Run server
```bash
uvicorn app.main:app --reload
```

## Models
| Model                      | Max Sequence Length: | Dimensions: | Speed (sentence/sec): | Size (MB): |
| -------------------------- | -------------------- | ----------- | --------------------- | ---------- |
| all-MiniLM-L6-v2           | 256                  | 384         | 14200                 | 80         |
| all-mpnet-base-v2          | 384                  | 768         | 2800                  | 420        |
| all-distilroberta-v1       | 512                  | 768         | 4000                  | 290        |
| multi-qa-distilbert-cos-v1 | 512                  | 768         | 4000                  | 250        |
| e5-large                   | 512                  | 1024        |                       | 1340       |

## Results
- All targets samples: 590
- Broken samples: 153
- Unrelated samples: 202
- Target samples: 235

### L2 abstract
| Model                      | Precisions         | Top-K              | Top-1              |
| -------------------------- | ------------------ | ------------------ | ------------------ |
| all-MiniLM-L6-v2           | 0.211489           | 0.991489           | 0.991489           |
| all-mpnet-base-v2          | 0.215319           | 0.995744           | 0.995744           |
| all-distilroberta-v1       | 0.21787            | 0.991489           | 0.991489           |
| multi-qa-distilbert-cos-v1 | 0.1914893          | 0.978723           | 0.970212           |
| e5-large                   | 0.2246808510638298 | 0.9829787234042553 | 0.9829787234042553 |
| Random                     | 0.0212             | 0.0025             | 0.0                |

### L2 title
| Model                      | Precisions        | Top-K              | Top-1              |
| -------------------------- | ----------------- | ------------------ | ------------------ |
| all-MiniLM-L6-v2           | 0.172340          | 0.778723           | 0.365957           |
| all-mpnet-base-v2          | 0.189361          | 0.812765           | 0.497872           |
| all-distilroberta-v1       | 0.17489           | 0.778723           | 0.387234           |
| multi-qa-distilbert-cos-v1 | 0.1446808         | 0.651063           | 0.357446           |
| e5-large                   | 0.214468085106383 | 0.8595744680851064 | 0.5872340425531914 |
| Random                     | 0.0212            | 0.0025             | 0.0                |


### Cosine abstract
| Model                      | Precisions         | Top-K              | Top-1              |
| -------------------------- | ------------------ | ------------------ | ------------------ |
| all-MiniLM-L6-v2           | 0.21148            | 0.991489           | 0.991489           |
| all-mpnet-base-v2          | 0.21531            | 0.995744           | 0.995744           |
| all-distilroberta-v1       | 0.21787            | 0.991489           | 0.991489           |
| multi-qa-distilbert-cos-v1 | 0.191489           | 0.978723           | 0.970212           |
| e5-large                   | 0.2246808510638298 | 0.9829787234042553 | 0.9829787234042553 |
| Random                     | 0.0212             | 0.0025             | 0.0                |

### Cosine title
| Model                      | Precisions   | Top-K          | Top-1          |
| -------------------------- | ------------ | -------------- | -------------- |
| all-MiniLM-L6-v2           | 0.17191      | 0.778723       | 0.365957       |
| all-mpnet-base-v2          | 0.189361     | 0.812765       | 0.497872       |
| all-distilroberta-v1       | 0.174893     | 0.778723       | 0.387234       |
| multi-qa-distilbert-cos-v1 | 0.144680     | 0.651063       | 0.357446       |
| e5-large                   | 0.2144680851 | 0.859574468085 | 0.587234042553 |
| Random                     | 0.0212       | 0.0025         | 0.0            |
