FROM python:3.9

# Location of source code
ENV PROJECT_ROOT /opt/app/
RUN mkdir -p $PROJECT_ROOT
WORKDIR $PROJECT_ROOT

# Copying dependencies
COPY ./requirements.txt .
COPY ./main.py .
COPY ./.env .

RUN pip install setuptools wheel
RUN pip install -r requirements.txt

COPY ./auth ./auth
COPY ./routes ./routes
COPY ./database ./database

RUN pip install --upgrade pip
RUN apt-get update -y && \
    apt-get install -y vim curl && \
    rm -rf var/lib/apt/lists/* \