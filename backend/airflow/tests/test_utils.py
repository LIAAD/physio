from src.utils import token_count, add_references

from examples import add_references_example


def test_token_count():
    text = "Hello, world!"
    n_tokens = token_count(text)
    expected_n_tokens = 4
    assert n_tokens == expected_n_tokens


def test_add_refrences():
    text = add_references_example["text"]
    pages = add_references_example["pages"]
    text_with_refs = add_references(text, pages)
    assert isinstance(text_with_refs, str)
