FROM python:3.10.5-slim-bullseye as builder
RUN apt-get -y update && \
    apt-get install  --no-install-recommends -y \
    curl \
    git \
    openssh-client=1:8.* \
    && \
    apt-get clean && \
    mkdir -p ~/.ssh && chmod 0600 -R ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts

COPY ./base_requirements.txt /base_requirements.txt
RUN pip install -r base_requirements.txt


FROM builder as base
COPY ./app/sentiment/requirements.txt /requirements.txt
RUN pip install -r requirements.txt


FROM base
COPY ./app ./app
COPY ./model-research/phobert-base-vietnamese-sentiment/phobert-base-vietnamese-sentiment ./app/sentiment/phobert-base-vietnamese-sentiment
WORKDIR /app
ENTRYPOINT ["celery",  "-A",  "sentiment", "worker",  "-l",  "INFO"]