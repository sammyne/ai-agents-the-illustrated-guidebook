import os
from typing import Type

from crewai import Agent, Crew, Process, Task
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from config import Config

c = Config()
llm = c.new_crewai_llm()


class CurrencyConverterInput(BaseModel):
    """
    Input schema for CurrencyConverterTool.
    """

    amount: float = Field(..., description="The amount to convert")
    from_currency: str = Field(
        ..., description="The source currency code (e.g., 'USD')"
    )
    to_currency: str = Field(..., description="The target currency code (e.g., 'EUR')")


class CurrencyConverterTool(BaseTool):
    name: str = "Currency Converter Tool"
    description: str = "Converts an amount from one currency to another"
    args_schema: Type[BaseModel] = CurrencyConverterInput
    api_key: str | None = os.getenv("EXCHANGE_RATE_API_KEY")

    def _run(self, amount: float, from_currency: str, to_currency: str) -> str:
        """
        Converts an amount from one currency to another.
        """
        import requests

        url = (
            f"https://v6.exchangerate-api.com/v6/{self.api_key}/latest/{from_currency}"
        )
        response = requests.get(url)

        if response.status_code != 200:
            raise Exception(f"Error: {response.status_code}")

        data = response.json()

        if (
            "conversion_rates" not in data
            or to_currency not in data["conversion_rates"]
        ):
            raise Exception(f"Invalid currency code: {to_currency}")

        rate = data["conversion_rates"][to_currency]
        converted_amount = amount * rate
        return (
            f"{amount} {from_currency} is equal to {converted_amount:.2f} {to_currency}"
        )


currency_analyst = Agent(
    role="Currency Analyst",
    goal="Provide real-time currency conversions and finacial analysis",
    backstory=(
        "You are a finace expert with deep knowledge of global exchange rates."
        "You help users with currency conversions and finacial decision-making."
    ),
    tools=[CurrencyConverterTool()],
    llm=llm,
    verbose=True,
)

currency_conversion_task = Task(
    description=(
        "Convert {amount} {from_currency} to {to_currency} "
        "using real-time exchange rates."
        "Provide the equivalent amount and explain any relevant financial context."
    ),
    expected_output=(
        "A detailed response including the converted amount and financial insights."
    ),
    agent=currency_analyst,
)

crew = Crew(
    agents=[currency_analyst],
    tasks=[currency_conversion_task],
    process=Process.sequential,
)

response = crew.kickoff(
    inputs={"amount": 100, "from_currency": "USD", "to_currency": "EUR"}
)
print(response)
