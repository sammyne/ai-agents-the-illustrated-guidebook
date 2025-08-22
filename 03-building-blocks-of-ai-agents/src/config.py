import os

import dotenv
from crewai import LLM


class Config:
    def __init__(self):
        dotenv.load_dotenv()

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("No API key found. Please check your .env file.")

        base_url = os.getenv("OPENAI_API_BASE_URL")
        if not base_url:
            raise ValueError("No base URL found. Please check your .env file.")

        model = os.getenv("OPENAI_MODEL")
        if not model:
            raise ValueError("No model found. Please check your .env file.")

        self.api_key = api_key
        self.base_url = base_url
        self.model = model

    def new_crewai_llm(self) -> LLM:
        return LLM(model=self.model, api_key=self.api_key, base_url=self.base_url)
