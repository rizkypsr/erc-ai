from textwrap import dedent
from crewai import Agent
from langchain_openai import ChatOpenAI

from crews.fg_index_crew.tools.create_fg_chart_tool import CreateFGChartTool


class Agents:
    def __init__(self):
        self.gpt_4o = ChatOpenAI(model="gpt-4o", temperature=0.5)

    def fg_analyst(self) -> Agent:
        return Agent(
            llm=self.gpt_4o,
            role="Cryptocurrency Fear and Greed Index Analyst",
            goal="Your goal or task is to perform a comprehensive analysis on the Fear and Greed Index for the specified cryptocurrency from the number index.",
            backstory=dedent("""
                As a Cryptocurrency Fear and Greed Index Analyst, you possess deep expertise in analyzing and interpreting Fear and Greed Index charts for cryptocurrencies. 
                Your role involves evaluating the performance of a specified cryptocurrency based on its Fear and Greed Index chart, which is provided as a screenshot. 
                You are adept at identifying key trends, patterns, and anomalies within the index data. 
                Your analysis should consider various factors such as index values, trend direction, and historical performance. 
                You will use this analysis to make informed recommendations on potential buy or sell actions based on the observed trends and index movements.
                Additionally, you are skilled in contextualizing your findings within broader market trends and offering actionable insights to help in strategic decision-making. Your ultimate goal is to provide a detailed and accurate assessment of the cryptocurrency's performance as reflected by its Fear and Greed Index.
            """),
            tools=[CreateFGChartTool()],
            verbose=True,
        )
