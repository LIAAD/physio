"""Pipeline DAG."""
import json
import logging
from difflib import get_close_matches
from pathlib import Path

import pendulum
from pymongo import MongoClient
import os

from airflow.decorators import dag, task
from airflow.operators.empty import EmptyOperator
from airflow.utils.edgemodifier import Label
from src.conf import DEFAULT_ANSWER
from src.models import GPT
from src.prompts import (
    medication_template,
    summary_template,
    validate_input_template,
    entity_extraction_template
)
from src.utils import get_top_pages, add_references
import dotenv

CURRENT_PATH = Path(__file__).parent

dotenv.load_dotenv(dotenv_path=CURRENT_PATH)

MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_URL = os.getenv("MONGO_URL")
MONGO_ENDPOINT = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_URL}"

MONGO_CLIENT = MongoClient(MONGO_ENDPOINT)
MONGO_DB = MONGO_CLIENT["physio"]

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

RESOURCE_PATH = Path("/app/resources")
CONDITIONS = json.loads((RESOURCE_PATH / "conditions.json").read_text())
MEDICATIONS = (RESOURCE_PATH / "medications.txt").read_text().split("\n")

MODEL = GPT(model="gpt-4", temperature=1)


@task
def parse_config(**kwargs) -> list:
    conf = kwargs["dag_run"].conf
    chat = conf["chat"]
    return chat


@task.branch
def validate_input(chat: str) -> bool:
    """Assert that the question is related to physical rehabilitation."""
    latest_question = chat['last_question']
    prompt = validate_input_template.substitute(question=latest_question)
    is_valid = MODEL(prompt)
    if is_valid.lower() == "true":
        return "entity_extraction"
    return "default_behavior"


@task
def entity_extraction(chat) -> str:
    """Extracts data from the source."""
    prompt = entity_extraction_template.substitute(question=chat["last_question"])
    logger.debug(f"Prompting model with:\n\n{prompt}\n\n")
    entity = MODEL(prompt)
    return entity


@task
def entity_linking(entity):

    logger.debug(f"Looking for entity {entity} in conditions list.")
    matches = get_close_matches(entity.lower(), CONDITIONS.keys(), 1)
    if matches:
        entity = matches[0]
        linked_entity = CONDITIONS[entity]["db_key"]
        return linked_entity

    logger.debug(f"Looking for entity {entity} in alias list.")
    for condition, info in CONDITIONS.items():
        logger.debug(f"\tLooking for entity {entity} in {condition} alias list.")
        matches = get_close_matches(entity.lower(), info["alias"], 1)
        if matches:
            logger.debug("Found a match.")
            linked_entity = info["db_key"]
            return linked_entity

    logger.debug(f"Looking for entity {entity} in every condition.")
    for condition in CONDITIONS.keys():
        if entity.lower() in condition:
            logger.debug("Found a match.")
            linked_entity = CONDITIONS[condition]["db_key"]
            return linked_entity

    logger.debug(f"Looking for entity {entity} in every condition alias.")
    for condition, info in CONDITIONS.items():
        logger.debug(f"\tLooking for entity {entity} in {condition} alias list.")
        if entity.lower() in str(info["alias"]):
            logger.debug("Found a match.")
            linked_entity = info["db_key"]
            return linked_entity


@task
def get_exercises(linked_entity: str):

    if linked_entity is None:
        return None

    collection = MONGO_DB.conditions
    content = collection.find_one({"name": linked_entity})
    exercises = content["exercises"][:5]  # TODO: random.shuffle
    return exercises


@task
def get_medication(chat: dict, linked_entity: str):

    prompt = medication_template.substitute(
        question=chat["last_question"],
        entity=linked_entity
    )

    medication_str = MODEL(prompt)
    logger.debug(f"Medication: {medication_str}")
    try:
        medication = json.loads(medication_str)
    except json.decoder.JSONDecodeError:
        return None

    collection = MONGO_DB.drugs

    medication = [med.lower() for med in medication]

    fuzzy_matches = []
    for m in medication:
        match = get_close_matches(m, MEDICATIONS, 1)
        if match:
            fuzzy_matches.append(match[0])

    matches = collection.find({"Generic Name": {"$in": fuzzy_matches}})
    medications = []
    for m in list(matches)[:5]:
        m.pop("_id")
        medications.append(m)

    return medications


@task
def get_summary(chat: str, linked_entity: str):

    if linked_entity is None:
        return None

    last_question = chat['last_question']
    collection = MONGO_DB.webpages

    content = collection.find_one({"name": linked_entity})

    if content is not None:

        pages = content["pages"]

        top_pages = get_top_pages(
            pages,
            last_question
        )

        prompt = summary_template.substitute(
            question=chat["last_question"],
            bodies=[page["body"] for page in top_pages],
        )

        answer = MODEL(prompt)
        answer_with_refs, top_pages = add_references(answer, top_pages)

        summary = {
            "text": answer_with_refs,
            "urls": top_pages
        }
    else:
        prompt = summary_template.substitute(
            question=chat["last_question"],
            bodies=[],
        )

        answer = MODEL(prompt)
        summary = {
            "text": answer,
            "urls": []
        }

    return summary

@task
def default_behavior() -> dict:
    return {
        "answer": {'text': DEFAULT_ANSWER},
        "exercises": None,
        "medications":  None,
    }


@task
def compile_content(exercises, medications, summary) -> dict:
    return {
        "answer": summary,
        "exercises": exercises,
        "medications": medications,
    }


@task
def store_answer_in_db(result: dict, **kwargs) -> None:
    """Stores the answer in mongo database."""
    rid = kwargs["run_id"]
    collection = MONGO_DB["results"]
    collection.insert_one({"rid": rid, "result": result})


@dag(
    tags=["pipeline"],
    start_date=pendulum.datetime(2021, 1, 1),
    schedule=None,
    catchup=False,
)
def pipeline():

    start = EmptyOperator(task_id="start")

    chat = parse_config()
    validation = validate_input(chat)

    start >> chat >> validation

    extracted_entity = entity_extraction(chat)
    linked_entity = entity_linking(extracted_entity)
    exercises = get_exercises(linked_entity)
    medications = get_medication(chat, linked_entity)  # TODO: fix medication
    summary = get_summary(chat, linked_entity)
    answer = compile_content(exercises, medications, summary)
    result = store_answer_in_db(answer)

    end = EmptyOperator(task_id="end")

    validation >> \
        Label("valid_question") >> \
        extracted_entity >> \
        exercises >> \
        medications >> \
        summary >> \
        answer >> \
        result >> \
        end

    default_answer = default_behavior()
    result = store_answer_in_db(default_answer)
    validation >> \
        Label("not_valid_question") >> \
        default_answer >> \
        result >> \
        end


pipeline()
