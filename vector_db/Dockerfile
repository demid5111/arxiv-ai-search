FROM python:3.10

ENV DB_PATH='/chroma'

WORKDIR /usr/src/app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0" ]
