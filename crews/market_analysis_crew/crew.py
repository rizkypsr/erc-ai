from crewai import Crew
from langchain_openai import ChatOpenAI

from crews.market_analysis_crew.agents import Agents
from crews.market_analysis_crew.tasks import Tasks


class MarketAnalysisCrew:
    def __init__(self, coin: str):
        self.gpt_4o = ChatOpenAI(model="gpt-4o", temperature=0.5)
        self.agent = Agents(coin=coin)
        self.tasks = Tasks()
        self.coin = coin

    def crew(self) -> Crew:
        """Creates the MarketAnalysisCrew crew"""

        market_analyst = self.agent.market_analyst()
        market_analysis_task = self.tasks.market_analysis(
            agent=market_analyst, coin=self.coin
        )

        return Crew(
            agents=[market_analyst],
            tasks=[market_analysis_task],
            verbose=True,
        )
