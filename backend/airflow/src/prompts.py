"""Prompts to be used as part of the extraction."""

from string import Template


validate_input_template = Template(
    """You are an assistant in the treatment of patients with physical pain or discomfort.
Your goal is to validate if the question is related to physical rehabilitation. 
Return True in case it is and False otherwise.

INPUT: $question
OUTPUT: """)


entity_extraction_template = Template(
    """You are an assistant in the treatment of patients with physical pain or discomfort.
Your goal is to extract the main topic of the question. 
Bellow follows some examples:

INPUT: How can I relieve my back pain?
OUTPUT: back pain

INPUT: I sprained my ankle. what can I do?
OUTPUT: ankle sprain

INPUT: do you recommend any medication for torn ligaments?
OUTPUT: torn ligaments

INPUT: should i stretch my arms?
OUTPUT: arm stretch

INPUT: $question
OUTPUT: """
)


medication_template = Template(
    """You are an assistant in the treatment of patients with physical pain or discomfort.
Your goal is to recommend over-the-counter medication for the patient given a question and the extracted entity. 
Do not recommend medication if the question does not require it.
The answer should be a list of medications.
Bellow follows some examples:

QUESTION: How can I relieve my back pain?
ENTITY: back pain
MEDICATION: ["ibuprofen", "acetaminophen"]

QUESTION: should i stretch my arms?
ENTITY: arms
MEDICATION: []

QUESTION: $question
ENTITY: $entity
MEDICATION: """
)

summary_template = Template(
    """You are an assistant in the treatment of patients with physical pain or discomfort.
Your task is generating an answer the user question based on the documents provided.
QUESTION: $question
DOCUMENTS: $bodies
ANSWER:
"""
)
