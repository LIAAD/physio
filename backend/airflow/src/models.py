"""All models used."""

import os
from pathlib import Path

import dotenv
import openai

from src.utils import token_count

ROOT = Path(__file__).parent.parent

dotenv.load_dotenv(ROOT / ".env")
openai.api_key = os.getenv("OPENAI_KEY")


class GPT:

    def __init__(
        self,
        model: str = "gpt-3.5-turbo",
        temperature: int = None,

    ) -> str:
        """ChatGPT model.
        args:
            model: model name [gpt3.5-turbo, gpt3.5-turbo-16k, gpt-4, gpt-4-32k]
            temperature: temperature of the model. 0 to 1
            engine: engine name [gpt35-team-2, gpt35-team-2-16k]

        """
        self.model = model
        self.temperature = temperature

        if "16k" in model:
            self.max_tokens = 16_384
        elif "32k" in model:
            self.max_tokens = 32_768
        else:
            self.max_tokens = 4_096

    def __call__(self, prompt: str, role: str = "system") -> str:
        """Generate text with ChatGPT."""

        n_tokens = token_count(prompt) + 7
        max_tokens_to_generate = self.max_tokens - n_tokens - 1
        tokens_to_generate = min(max_tokens_to_generate, n_tokens + 1_000)

        message = [{"role": role, "content": f"{prompt}"}]

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=message,
            temperature=self.temperature,
            max_tokens=tokens_to_generate,
        )

        content = response.to_dict()
        answer = content["choices"][0]["message"]["content"]

        return answer
