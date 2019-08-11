FROM python:3.7-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY heroku.yml .
COPY repo_replicator .

ENTRYPOINT ["python", "-m", "repo_replicator"]