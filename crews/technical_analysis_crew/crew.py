from crewai import Crew
from langchain_openai import ChatOpenAI

from crews.technical_analysis_crew.agents import Agents
from crews.technical_analysis_crew.tasks import Tasks


class TechnicalAnalysisCrew:
    def __init__(self, coin: str):
        self.gpt_4o = ChatOpenAI(model="gpt-4o", temperature=0.5)
        self.agent = Agents(coin=coin)
        self.tasks = Tasks()
        self.coin = coin

    def crew(self) -> Crew:
        """Creates the TechnicalAnalysisCrew crew"""

        chart_analyst = self.agent.chart_analyst()
        chart_analysis_task = self.tasks.chart_analysis_task(
            agent=chart_analyst, coin=self.coin
        )

        return Crew(
            agents=[chart_analyst],
            tasks=[chart_analysis_task],
            verbose=True,
        )
