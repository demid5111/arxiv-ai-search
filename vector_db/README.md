# vector-db-service

## Running locally

1. Change current directory: `cd vector_db` 
2. Run server
```bash
uvicorn app.main:app --reload
```

## Deploy

1. Build docker image
```bash
cd vector_db
docker build -t vector_db .
```
2. Run image with DB
```bash
docker run -v {PATH_TO_DB}:/chroma -p 8000:8000 vector_db
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
- All in csv 566847
- Without broken 566844
- All targets samples: 590
- Broken samples: 153
- Unrelated samples: 202
- Target samples: 235

### L2 abstract
| Model                      | Precisions | Top-K  | Top-1  |
| -------------------------- | ---------- | ------ | ------ |
| all-MiniLM-L6-v2           | 0.2115     | 0.9916 | 0.9915 |
| all-mpnet-base-v2          | 0.2153     | 0.9957 | 0.9957 |
| all-distilroberta-v1       | 0.2179     | 0.9915 | 0.9915 |
| multi-qa-distilbert-cos-v1 | 0.1915     | 0.9787 | 0.9702 |
| e5-large                   | 0.2247     | 0.9830 | 0.9830 |
| Random                     | 0.0212     | 0.0025 | 0.0    |

### L2 title
| Model                      | Precisions | Top-K  | Top-1  |
| -------------------------- | ---------- | ------ | ------ |
| all-MiniLM-L6-v2           | 0.1723     | 0.7787 | 0.3660 |
| all-mpnet-base-v2          | 0.1893     | 0.8128 | 0.4979 |
| all-distilroberta-v1       | 0.1749     | 0.7787 | 0.3872 |
| multi-qa-distilbert-cos-v1 | 0.1447     | 0.6511 | 0.3574 |
| e5-large                   | 0.2145     | 0.8596 | 0.5872 |
| Random                     | 0.0212     | 0.0025 | 0.0    |


### Cosine abstract
| Model                      | Precisions | Top-K  | Top-1  |
| -------------------------- | ---------- | ------ | ------ |
| all-MiniLM-L6-v2           | 0.2114     | 0.9915 | 0.9915 |
| all-mpnet-base-v2          | 0.2153     | 0.9957 | 0.9957 |
| all-distilroberta-v1       | 0.2179     | 0.9915 | 0.9915 |
| multi-qa-distilbert-cos-v1 | 0.1915     | 0.9787 | 0.9702 |
| e5-large                   | 0.2247     | 0.9830 | 0.9830 |
| Random                     | 0.0212     | 0.0025 | 0.0    |

### Cosine title
| Model                      | Precisions | Top-K  | Top-1  |
| -------------------------- | ---------- | ------ | ------ |
| all-MiniLM-L6-v2           | 0.1719     | 0.7787 | 0.3660 |
| all-mpnet-base-v2          | 0.1894     | 0.8128 | 0.4979 |
| all-distilroberta-v1       | 0.1749     | 0.7787 | 0.3872 |
| multi-qa-distilbert-cos-v1 | 0.1447     | 0.6511 | 0.3574 |
| e5-large                   | 0.2145     | 0.8596 | 0.5872 |
| Random                     | 0.0212     | 0.0025 | 0.0    |


## Query results
Query: LoRA: Low-Rank Adaptation of Large Language Models
| Result | Article                                                                                          |
| ------ | ------------------------------------------------------------------------------------------------ |
|        | Low-rank Adaptation of Large Language Model Rescoring for Parameter-Efficient Speech Recognition |
|        | QA-LoRA: Quantization-Aware Low-Rank Adaptation of Large Language Models                         |
|        | The Expressive Power of Low-Rank Adaptation                                                      |
|        | Orthogonal Subspace Learning for Language Model Continual Learning                               |
|        | VeRA: Vector-based Random Matrix Adaptation                                                      |
|        | LoraHub: Efficient Cross-Task Generalization via Dynamic LoRA Composition                        |
|        | Parameter-Efficient Multilingual Summarisation: An Empirical Study                               |
|        | Delta-LoRA: Fine-Tuning High-Rank Parameters with the Delta of Low-Rank Matrices                 |
|        | Low-rank Adaptation Method for Wav2vec2-based Fake Audio Detection                               |
|        | LoRA: Low-Rank Adaptation of Large Language Models                                               |

## Hardware and Software
Hardware used for experiments: CPU: AMD Ryzen 3 PRO 3200G X4 3.6Gh, GPU: NVIDIA GeForce RTX 3060 12Gb. Software used for experiments: Driver Version: 525.147.05,  CUDA Version: 12.0.
