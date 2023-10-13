from string import Template
from src.prompts import (
    entity_extraction_template,
    validate_input_template,
    medication_template
)
from src.models import GPT


MODEL = GPT()


def _inference(question: str, template: Template) -> str:
    prompt = template.substitute(question=question)
    answer = MODEL(prompt)
    return answer


def test_validate_input_template_true():
    question = "should i stretch my arms?"
    is_valid = _inference(question, validate_input_template)
    assert is_valid.lower() == "true"


def test_validate_input_template_not_english():
    question = "estou com dores nas costas."
    prompt = validate_input_template.substitute(question=question)
    is_valid = MODEL(prompt)
    assert is_valid.lower() == "false"
    

def test_validate_input_template_false():
    question = "How are you today"
    is_valid = _inference(question, validate_input_template)
    assert is_valid.lower() == "false"


def test_condition_template_arm():
    question = "should i stretch my arms?"
    condition = _inference(question, entity_extraction_template)
    assert condition.lower() in ["arm stretch", "arm stretching"]


def test_chat_template():
    question = 'I sprained my ankle. what can I do?'
    entity = 'ankle sprain'
    prompt = medication_template.substitute(
        question=question,
        entity=entity
    )
    answer = MODEL(prompt)
    assert isinstance(answer, str)
