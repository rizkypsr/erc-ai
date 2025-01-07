from textwrap import dedent
from crewai import Agent
from langchain_openai import ChatOpenAI
from crewai_tools import ScrapeWebsiteTool


class Agents:
    def __init__(self, coin: str):
        self.gpt_4o = ChatOpenAI(model="gpt-4o", temperature=0.5)
        self.coin = coin

    def market_analyst(self) -> Agent:
        print("xxxxxxx")
        print(f"xxxxxxx https://coinmarketcap.com/currencies/{self.coin}/")
        return Agent(
            llm=self.gpt_4o,
            role="Cryptocurrency Market Analysis Specialist",
            goal="Perform a comprehensive market analysis for the specified cryptocurrency.",
            backstory=dedent("""
                You are a fundamental analyzer of cryptocurrency with a deep understanding of the cryptocurrency landscape. Your role involves
                utilizing an API to fetch real-time data from a designated website. Your expertise
                lies in transforming this data into precise required values. Then generate a response using that values."""),
            tools=[
                ScrapeWebsiteTool(
                    website_url=f"https://coinmarketcap.com/currencies/{self.coin}/"
                )
            ],
            verbose=True,
        )
