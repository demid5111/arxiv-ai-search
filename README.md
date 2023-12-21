# Semantic search of similar academic papers

![CI workflow](https://github.com/demid5111/arxiv-ai-search/actions/workflows/ci_pipeline.yml/badge.svg)

> **DISCLAIMER**: This is a project made during the ODS.ai course 
> [Natural Language Processing](https://ods.ai/tracks/nlp-course-autumn-23), Autumn 2023.

MVP of a service is available online: [http://62.84.112.56:8000/](http://62.84.112.56:8000/)

## Authors

1. Demidovskij Alexander Vladimirovich
2. Salnikov Igor Gennadievich

## Whitepaper report

It is prepared as a LaTeX project, sources are placed in [./report/main.tex](./report/main.tex).
Currently, built version is placed in [./report/main.pdf](./report/main.pdf)

## Validation dataset

Validation dataset is collected with web scraping techniques and is placed in
[./arxiv_scrapper/assets](./arxiv_scrapper/assets/arxiv_google_Nov_2023.csv).
The way it is collected is described in report, source code is placed in
[./arxiv_scrapper/scrapper_search.py](./arxiv_scrapper/scrapper_search.py)

## arXiv index

arXiv search service that we designed is working on top of own arXiv index for the category
"Computer Science". Index is placed in
[cloud](https://cloud.mail.ru/public/MrJu/TW2mYSV55/arxiv_abs_Nov_2023.csv).
The way it is collected is described in report, source code is placed in
[./arxiv_scrapper/scrapper_index.py](./arxiv_scrapper/scrapper_index.py)

## Model selection

After performing comparison study among available encoder models on HuggingFace, we have chosen
**e5-large** model. See report for details.

### Framework selection

Solution is based on:

1. [FastAPI](https://fastapi.tiangolo.com/) - framework for building web applications
   that expose REST API and serve static files
2. [Bootstrap](https://getbootstrap.com/) - library for building responsive UI for web applications
3. [PyTorch](https://pytorch.org/) - framework for designing DL pipelines, training and inference
   of DL models
5. [Docker](https://www.docker.com/) - containerizing solution for web applications

### MVP for arXiv search

Application code is located in [./vector_db/app](./vector_db/app) folder:

* [./vector_db/static](./vector_db/static) - UI for application
* [./vector_db/app/main.py](./vector_db/app/main.py) - server code with all REST API endpoint

Deployed as a web application: [http://158.160.28.22/](http://62.84.112.56:8000/)

All deployment instructions are present in [./vector_db/README.md](./vector_db/README.md).

## Code quality

Code quality is automatically (per each PR/push to main branch) checked with:

1. [GitHub Actions](https://github.com/features/actions) - platform for running automated checks
2. [mypy](https://pypi.org/project/mypy/) - library for static type checking
3. [pylint](https://pypi.org/project/pylint/) - library for evaluating code style
   (traditional and well-respected)
4. [flake8](https://pypi.org/project/flake8/) - library for evaluating code style
   (primarily imports order and completeness)
