FROM python:3.7-alpine

WORKDIR /app

ENV PYTHONPATH=.

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY heroku.yml /app/heroku.yml
COPY repo_replicator /app/repo_replicator

ENTRYPOINT ["python", "-m", "repo_replicator"]