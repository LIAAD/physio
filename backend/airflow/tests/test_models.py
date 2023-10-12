from src.models import GPT


def test_chatgpt():
    prompt = "Write hello."
    chatgpt = GPT(model="gpt-3.5-turbo")
    answer = chatgpt(prompt)
    assert isinstance(answer, str)


def test_gpt4():
    prompt = "Write hello."
    chatgpt = GPT(model="gpt-4")
    answer = chatgpt(prompt)
    assert isinstance(answer, str)
