FROM python:3.11-slim

WORKDIR /src
RUN apt-get update  \
    && apt-get install gcc build-essential -y
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt /src/
COPY opik.config /home
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

COPY ./app ./app
COPY ./faiss_indexes ./faiss_indexes
CMD PYTHONPATH=. python app/main.py

