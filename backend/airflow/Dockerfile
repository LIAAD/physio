FROM apache/airflow:2.6.3-python3.10

WORKDIR /app

COPY . .

USER root
RUN apt-get update && apt-get clean 

USER airflow
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m nltk.downloader punkt
RUN pip install -e .

