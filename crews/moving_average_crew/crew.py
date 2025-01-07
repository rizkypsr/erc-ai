from crewai import Crew
from langchain_openai import ChatOpenAI

from crews.moving_average_crew.agents import Agents
from crews.moving_average_crew.tasks import Tasks


class MovingAverageCrew:
    def __init__(self, coin: str):
        self.gpt_4o = ChatOpenAI(model="gpt-4o", temperature=0.5)
        self.agent = Agents(coin=coin)
        self.tasks = Tasks()
        self.coin = coin

    def crew(self) -> Crew:
        """Creates the MovingAverageCrew crew"""

        moving_average_analyst = self.agent.moving_average_analyst()
        moving_average_analysis = self.tasks.moving_average_analysis(
            agent=moving_average_analyst, coin=self.coin
        )

        return Crew(
            agents=[moving_average_analyst],
            tasks=[moving_average_analysis],
            verbose=True,
        )
