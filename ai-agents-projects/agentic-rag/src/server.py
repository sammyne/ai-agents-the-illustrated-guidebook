# rename .env.example to .env and add the following:
# SERPER_API_KEY=your_serper_api_key
# OPENAI_API_KEY=your_openai_api_key

from crewai import Crew, Agent, Task
import litserve as ls

# 可用的工具列表参见 https://docs.crewai.com/en/concepts/tools#available-crewai-tools

from config import Config

# If you'd like, you can use a local LLM as well through Ollama. Do this:
# ollama pull qwen3 in the command line.

# Uncomment the following line and also the llm=llm line in the Agents definitions.
# llm = LLM(model="ollama/qwen3")

# 使用硅基流动的 API
c = Config()
llm = c.new_llm()


class AgenticRAGAPI(ls.LitAPI):
    def setup(self, device):
        researcher_agent = Agent(
            role="Researcher",
            goal="Research about the user's query and generate insights",
            backstory="You are a helpful assistant that can answer questions about the document.",
            verbose=True,
            tools=[c.new_tavily()],
            llm=llm,
        )

        writer_agent = Agent(
            role="Writer",
            goal="Use the available insights to write a concise and informative response to the user's query",
            backstory="You are a helpful assistant that can write a report about the user's query",
            verbose=True,
            llm=llm,
        )

        researcher_task = Task(
            description="Research about the user's query and generate insights: {query}",
            expected_output="A concise and informative report about the user's query",
            agent=researcher_agent,
        )

        writer_task = Task(
            description="Use the available insights to write a concise and informative response to the user's query: {query}",
            expected_output="A concise and informative response to the user's query",
            agent=writer_agent,
        )

        self.crew = Crew(
            agents=[researcher_agent, writer_agent],
            tasks=[researcher_task, writer_task],
            verbose=True,
        )

    def decode_request(self, request, **kwargs):
        return request["query"]

    def predict(self, x, **kwargs):
        return self.crew.kickoff(inputs={"query": x})

    def encode_response(self, output, **kwargs):
        return {"output": output}


if __name__ == "__main__":
    api = AgenticRAGAPI()
    server = ls.LitServer(api)
    server.run(port=8000)
