FROM python:3.10.5-slim-bullseye as apibuilder
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


FROM apibuilder
COPY ./app ./app
WORKDIR /app
RUN chmod +x ./prestart.sh