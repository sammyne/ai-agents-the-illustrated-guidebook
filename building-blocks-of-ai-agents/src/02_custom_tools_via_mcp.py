from crewai import Agent, Crew, Task
from crewai_tools import MCPServerAdapter

from config import Config

llm = Config().new_crewai_llm()

# 依赖命令 `uv run src/02_custom_tools_via_mcp_server.py` 部署的 MCP 服务器
server_params = {
    "url": "http://localhost:8081/sse",
    "transport": "sse",
}

# 参考文献：https://docs.crewai.com/en/mcp/multiple-servers
try:
    with MCPServerAdapter(server_params) as mcp_tools:
        currency_agent = Agent(
            role="Currency Analyst",
            goal="Convert currency using real-time exchange rates.",
            backstory=(
              "You help users convert between currencies using up-to-date market data."
            ),
            allow_delegation=False,
            tools=[mcp_tools['convert_currency']],
            llm=llm,
        )

        conversion_task = Task(
            description=(
                    "Convert {amount} {from_currency} to {to_currency} "
                    "using real-time exchange rates."
                    "Provide the equivalent amount and explain any relevant financial context."
                ),
                expected_output=(
                    "A formatted result with exchange rate."
                ),
                agent=currency_agent,
        )

        crew = Crew(
            agents=[currency_agent],
            tasks=[conversion_task],
            verbose=True
        )

        result = crew.kickoff(
            inputs={
                "amount": 100,
                "from_currency": "USD",
                "to_currency": "CNY"
            }
        )
        print(result)
        
except Exception as e:
    print(e)
