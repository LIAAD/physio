FROM python:3.10

WORKDIR /app

COPY requirements.txt .

COPY cert.crt .
COPY cert.key .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

CMD [ "flask", "run", "--host=0.0.0.0", "--port=39873", "--cert=cert.crt", "--key=cert.key", "--debug" ]