import os

import dotenv
import requests
from mcp.server.fastmcp import FastMCP

dotenv.load_dotenv()

mcp = FastMCP("currency-converter-server", port=8081)

API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")


@mcp.tool()
def convert_currency(amount: float, from_currency: str, to_currency: str):
    """Converts currency using real-time exchange rates."""

    response = requests.get(
        f"https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{from_currency}/{to_currency}/{amount}"
    ).json()

    return f"{amount} {from_currency.upper()} = {response['conversion_result']:.2f} {to_currency.upper()} (Rate: {response['conversion_rate']:.4f})"

if __name__ == "__main__":
    mcp.run(transport="sse")
