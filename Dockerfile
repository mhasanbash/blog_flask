ARG PY_VERSION=3.10
FROM python:${PY_VERSION}
COPY . /app
WORKDIR /app

RUN pip3 install -r requirements.txt

RUN groupadd -r usergroup && useradd --no-log-init -r -g usergroup myuser

RUN apt-get update && apt-get install nano

USER root	

EXPOSE 5000

CMD ["python", "app.py"]
