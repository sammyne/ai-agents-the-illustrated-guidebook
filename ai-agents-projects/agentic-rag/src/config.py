import os

import dotenv
from crewai import LLM
from crewai_tools import TavilySearchTool


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

        tavily_api_key = os.getenv("TAVILY_API_KEY")
        if not tavily_api_key:
            raise ValueError("No Tavily API key found. Please check your .env file.")

        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.tavily_api_key = tavily_api_key

    def new_llm(self) -> LLM:
        return LLM(model=self.model, api_key=self.api_key, base_url=self.base_url)

    def new_tavily(self) -> TavilySearchTool:
        return TavilySearchTool(api_key=self.tavily_api_key)