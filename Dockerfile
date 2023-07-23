ARG PY_VERSION=3.10
FROM python:${PY_VERSION}

VOLUME /app
COPY . /app
WORKDIR /app

RUN pip3 install -r requirements.txt

#RUN apt-get update
#RUN apt-get install nano

RUN groupadd -r usergroup && useradd --no-log-init -r -g usergroup myuser

USER myuser	

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
