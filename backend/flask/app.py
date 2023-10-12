import os
import time
import logging
from pathlib import Path

import dotenv
import requests
from pymongo import MongoClient

from flask import Flask, request

from flask_cors import CORS

CURRENT_PATH = Path(__file__).parent

dotenv.load_dotenv(dotenv_path=CURRENT_PATH)

AIRFLOW_USER = os.getenv("AIRFLOW_USER")
AIRFLOW_PASSWORD = os.getenv("AIRFLOW_PASSWORD")
AIRFLOW_AUTH = (AIRFLOW_USER, AIRFLOW_PASSWORD)

AIRFLOW_WEBSERVER = os.getenv("AIRFLOW_WEBSERVER", "localhost:8080")
AIRFLOW_DAG_API = f'http://{AIRFLOW_WEBSERVER}/api/v1/dags/pipeline/dagRuns'

MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_URL = os.getenv("MONGO_URL")
MONGO_ENDPOINT = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_URL}"
CLIENT = MongoClient(MONGO_ENDPOINT)
DB = CLIENT["physio"]

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logging.debug("Start")

app = Flask(__name__)

cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'

CORS(app, resources=r'/*', headers='Content-Type')


def trigger_dag(chat: dict) -> str:

    logger.debug(f"Triggering DAG with chat: {chat}")

    response = requests.post(
        AIRFLOW_DAG_API,
        json={'conf': {
            "chat": chat,
        }},
        auth=AIRFLOW_AUTH
    )

    if response.status_code != 200:
        raise Exception(response.content)

    logger.debug("DAG triggered!")
    content = response.json()
    dag_run_id = content['dag_run_id']

    return dag_run_id


def wait_dag_completion(dag_run_id: str) -> None:

    logger.debug("Wating for DAG completion...")

    for _ in range(0, 120):
        logger.debug(
            f"Sending request to Airflow endpoint: {AIRFLOW_DAG_API}/{dag_run_id}")

        response = requests.get(
            f"{AIRFLOW_DAG_API}/{dag_run_id}",
            auth=AIRFLOW_AUTH
        )
        content = response.json()
        logger.debug(f"Response: {content}")

        if content["state"] == 'success':
            logger.debug("DAG completed!")
            return True

        elif content["state"] == 'failed':
            logger.debug("DAG failed!")
            return False

        logger.debug("Waiting for DAG completion...")
        time.sleep(1)

    return False


def retrieve_result(dag_run_id: str) -> dict:
    logger.debug("Retrieving result...")
    logger.debug(dag_run_id)
    collection = DB["results"]
    result = collection.find_one({"rid": dag_run_id})
    logger.debug(f"Result retrieved: {result}")
    return result


@app.route('/pipeline', methods=['POST'])
def pipeline():
    chat = request.json.get('chat')

    dag_run_id = trigger_dag(chat)

    if not wait_dag_completion(dag_run_id):
        return {"error": "DAG failed"}, 500

    result = retrieve_result(dag_run_id)

    if result is None:
        return {"error": "DAG failed"}, 500

    result.pop('_id', None)

    return result
