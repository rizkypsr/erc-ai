from textwrap import dedent
from crewai import Agent
from langchain_openai import ChatOpenAI

from crews.technical_analysis_crew.tools.analyze_chart import AnalyzeChart
from crews.technical_analysis_crew.tools.create_candlestick import CreateCandleStick


class Agents:
    def __init__(self, coin: str):
        self.gpt_4o = ChatOpenAI(model="gpt-4o", temperature=0.5)
        self.coin = coin

    def chart_analyst(self) -> Agent:
        return Agent(
            llm=self.gpt_4o,
            role="Cryptocurrency Chart Analysis Specialist",
            goal="Your goal or task is to perform a comprehensive Chart analysis for the specified cryptocurrency from its candlestick chart screenshot.",
            backstory=dedent("""
            You an automate the process of analyzing technical indicators (e.g.RSI, MACD) and 
            chart patterns to identify trends and potential buy or sell signals in cryptocurrency price charts. 
            These models can help traders make decisions based on technical analysis."""),
            tools=[
                CreateCandleStick(),
                AnalyzeChart(),
            ],
            verbose=True,
        )
